import typing as t

from selenium.webdriver.remote.webdriver import WebDriver

from ..abc import ABCFetcher


class SeleniumFetcher(ABCFetcher):
    def __init__(
        self,
        webdriver_class: type[WebDriver],
        webdriver_arguments: dict[str, t.Any] | None = None,
    ) -> None:
        if webdriver_arguments is None:
            webdriver_arguments = {}

        self._webdriver: WebDriver | None = None
        self._webdriver_class = webdriver_class
        self._webdriver_arguments = webdriver_arguments

    async def open(self) -> None:
        self._webdriver = self._webdriver_class(**self._webdriver_arguments)

    async def fetch(self, url: str) -> str:
        if not self.is_open():
            raise RuntimeError("Fetcher is not open")

        self._webdriver.get(url)
        return self._webdriver.page_source

    async def close(self) -> None:
        self._webdriver.close()
        self._webdriver = None

    def is_open(self) -> bool:
        return self._webdriver is not None
