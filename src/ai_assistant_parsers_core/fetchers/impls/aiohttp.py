from aiohttp import ClientSession

from ..abc import ABCFetcher


class AiohttpFetcher(ABCFetcher):
    def __init__(self, client: ClientSession) -> None:
        self._client = client

    async def fetch(self, url: str) -> str:
        async with self._client.get(url) as response:
            try:
                return await response.text()
            except UnicodeDecodeError:
                return await response.text(encoding="windows-1251")
