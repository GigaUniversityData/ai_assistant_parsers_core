"""Модуль для ``AiohttpFetcher``."""

import typing as t
from contextlib import suppress

import charset_normalizer
from aiohttp import ClientSession
from aiohttp_retry import RetryClient, ListRetry

from ..abc import ABCFetcher


class AiohttpFetcher(ABCFetcher):
    """Фетчер на основе ``aiohttp``."""

    def __init__(self, client_arguments: dict[str, t.Any] | None = None) -> None:
        if client_arguments is None:
            client_arguments = {}

        self._client: ClientSession | None = None
        self._retry_client: RetryClient | None = None
        self._client_arguments = client_arguments

    async def open(self) -> None:
        """Открывает фетчер."""
        self._client = ClientSession(**self._client_arguments)
        self._retry_client = RetryClient(
            client_session=self._client,
            retry_options=ListRetry(timeouts=[1, 3, 5, 10]),
        )

    async def fetch(self, url: str) -> str:
        """Извлекает HTML из URL-адреса."""
        if not self.is_open():
            raise RuntimeError("Fetcher is not open")

        async with self._retry_client.get(url) as response:
            byte_string = await response.read()

            with suppress(UnicodeDecodeError):
                encoding = response.get_encoding()
                return byte_string.decode(encoding=encoding)

            with suppress(UnicodeDecodeError):
                return byte_string.decode(encoding="windows-1251")

            result = charset_normalizer.detect(byte_string)
            if result["encoding"] is not None:
                return byte_string.decode(encoding=result["encoding"])

            raise RuntimeError("The encoding could not be detected automatically") from None

    async def close(self) -> None:
        """Закрывает фетчер."""
        await self._client.close()
        self._client = None
        self._retry_client = None

    def is_open(self) -> bool:
        """Проверяет открыт ли фетчер."""
        return self._client is not None and self._retry_client is not None
