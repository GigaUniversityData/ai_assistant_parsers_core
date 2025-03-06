"""Модуль для ``APIFetcher``."""
import base64
from os import getenv

import brotli
from aiohttp import ClientSession

from ai_assistant_parsers_core.magic_url import MagicURL
from ..abc import ABCFetcher
from ..errors import FetcherError, FetcherNotOpenError, InvalidAuthorizationError


DEFAULT_API_URL = getenv("AAPC_FETCHING_API_URL", "http://5.35.3.148:8300/fetch")
API_TOKEN = getenv("AAPC_FETCHING_API_TOKEN")


class APIFetcher(ABCFetcher):
    """Фетчер на основе API сервера."""

    def __init__(self, api_url: str | None = None) -> None:
        self._api_url = DEFAULT_API_URL if api_url is None else api_url
        self._client: ClientSession | None = None

    async def open(self) -> None:
        """Открывает фетчер."""
        self._client = ClientSession(raise_for_status=True)

    async def fetch(self, magic_url: MagicURL) -> str:
        """Извлекает HTML из URL-адреса."""
        if not self.is_open():
            raise FetcherNotOpenError
        if API_TOKEN is None:
            # TODO: Названия ошибкам
            raise InvalidAuthorizationError(
                "Authorization parameters are not specified. "
                "Please use the 'AAPC_FETCHING_API_TOKEN' environment variable for this"
            )

        headers = {"Authorization": f"Basic {API_TOKEN}"}
        params = {"url": magic_url.url}  # TODO: Обдумать использование нормализованного URL
        try:
            async with self._client.get(self._api_url, headers=headers, params=params) as response:
                json = await response.json()
        except Exception as error:
            raise FetcherError(f"Unexpected error while fetching {magic_url.url}") from error

        return self._decore_raw_html(json["data"]["raw_html"])

    async def close(self) -> None:
        """Закрывает фетчер."""
        await self._client.close()
        self._client = None

    def is_open(self) -> bool:
        """Проверяет открыт ли фетчер."""
        return self._client is not None

    def _decore_raw_html(self, raw_html: str) -> str:
        decoded_once = base64.b64decode(raw_html)
        decoded_twice = base64.b64decode(decoded_once)

        raw_data = brotli.decompress(decoded_twice)
        text = raw_data.decode("utf-8", errors="replace")

        return text
