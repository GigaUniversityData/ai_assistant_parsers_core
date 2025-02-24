"""Модуль для ``APIFetcher``."""
from aiohttp import ClientSession

from ai_assistant_parsers_core.magic_url import MagicURL
from ..abc import ABCFetcher


API_DEFAULT_URL = "https://uniassistant.ru/api/fetching-api/fetch"


class APIFetcher(ABCFetcher):
    """Фетчер на основе API сервера."""

    def __init__(self, api_url: str | None = None) -> None:
        self._api_url = API_DEFAULT_URL if api_url is None else api_url
        self._client: ClientSession | None = None

    async def open(self) -> None:
        """Открывает фетчер."""
        self._client = ClientSession(raise_for_status=True)

    async def fetch(self, url: str) -> str:
        """Извлекает HTML из URL-адреса."""
        magic_url = MagicURL(url)
        if not self.is_open():
            raise RuntimeError("Fetcher is not open")

        async with self._client.get(magic_url.normalized_url) as response:
            json = await response.json()

        return json["raw_html"]

    async def close(self) -> None:
        """Закрывает фетчер."""
        await self._client.close()
        self._client = None

    def is_open(self) -> bool:
        """Проверяет открыт ли фетчер."""
        return self._client is not None
