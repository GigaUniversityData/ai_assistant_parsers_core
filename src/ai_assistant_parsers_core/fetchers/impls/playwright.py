"""Модуль для ``PlaywrightFetcher``."""

from playwright.async_api import async_playwright, Playwright, Browser

from ..abc import ABCFetcher


class PlaywrightFetcher(ABCFetcher):
    """Фетчер на основе ``playwright``."""

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    async def open(self) -> None:
        """Открывает фетчер."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.firefox.launch()

    async def fetch(self, url: str) -> str:
        """Извлекает HTML из URL-адреса."""
        if not self.is_open():
            raise RuntimeError("Fetcher is not open")

        page = await self._browser.new_page()
        await page.goto(url)
        content = await page.content()
        return content

    async def close(self) -> None:
        """Закрывает фетчер."""
        await self._browser.close()
        await self._playwright.stop()

    def is_open(self) -> bool:
        """Проверяет открыт ли фетчер."""
        return self._playwright is not None and self._browser is None
