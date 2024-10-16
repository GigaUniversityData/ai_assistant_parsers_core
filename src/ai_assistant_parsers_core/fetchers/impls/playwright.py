from playwright.async_api import Playwright

from ..abc import ABCFetcher


class PlaywrightFetcher(ABCFetcher):
    def __init__(self, client: Playwright) -> None:
        self._client = client

    async def fetch(self, url: str) -> str:
        browser = await self._client.chromium.launch()

        page = await browser.new_page()
        await page.goto(url)

        text = await page.evaluate("() => document.body.innerText")

        await browser.close()

        return text
