"""Модуль для ``APIFetcher``."""
import base64
import warnings
from os import getenv

import brotli
from aiohttp import ClientSession, ClientConnectorError, ClientResponseError

from ai_assistant_parsers_core.magic_url import MagicURL
from ai_assistant_parsers_core.common_utils.decode_body import decode_body
from ..abc import ABCFetcher
from ..errors import (
    FetcherNotOpenError,
    InvalidAuthorizationError,
    ServerConnectionError,
    ServerResponseError,
)


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
            raise InvalidAuthorizationError(
                "Authorization parameters are not specified. "
                "Please use the 'AAPC_FETCHING_API_TOKEN' environment variable for this"
            )

        headers = {"Authorization": f"Basic {API_TOKEN}"}
        params = {"url": magic_url.url}  # TODO: Обдумать использование нормализованного URL
        try:
            async with self._client.get(self._api_url, headers=headers, params=params) as response:
                json = await response.json()
        except ClientConnectorError as error:
            raise ServerConnectionError from error
        except ClientResponseError as error:
            raise ServerResponseError from error

        return self._decore_raw_html(json["data"]["raw_html"])

    async def close(self) -> None:
        """Закрывает фетчер."""
        await self._client.close()
        self._client = None

    def is_open(self) -> bool:
        """Проверяет открыт ли фетчер."""
        return self._client is not None

    def _decore_raw_html(self, raw_html: str) -> str:
        decoded_string = base64.b64decode(raw_html)

        try:
            raw_data_body = brotli.decompress(decoded_string)
        except brotli.error:
            warnings.warn(
                f"`raw_html` data is stored incorrectly on the server side. Please, contact the server developers."
            )
            raw_data_body = brotli.decompress(base64.b64decode(decoded_string))

        raw_html = decode_body(raw_data_body)
        return raw_html
