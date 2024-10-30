"""Модуль для ``SeleniumFetcher``."""

import typing as t

from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver, Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver, Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ..abc import ABCFetcher


class SeleniumFetcher(ABCFetcher):
    """Фетчер на основе ``selenium``."""

    def __init__(
        self,
        webdriver_class: type[ChromeWebDriver | FirefoxWebDriver],
        webdriver_arguments: dict[str, t.Any] | None = None,
    ) -> None:
        if webdriver_arguments is None:
            webdriver_arguments = {}

        self._webdriver: ChromeWebDriver | FirefoxWebDriver | None = None
        self._webdriver_class = webdriver_class
        self._webdriver_arguments = webdriver_arguments

    async def open(self) -> None:
        """Открывает фетчер."""
        self._add_headless_to_options()
        self._add_service_to_options()
        self._webdriver = self._webdriver_class(**self._webdriver_arguments)

    async def fetch(self, url: str) -> str:
        """Извлекает HTML из URL-адреса."""
        if not self.is_open():
            raise RuntimeError("Fetcher is not open")

        self._webdriver.get(url)
        return self._webdriver.page_source

    async def close(self) -> None:
        """Закрывает фетчер."""
        self._webdriver.quit()
        self._webdriver = None

    def is_open(self) -> bool:
        """Проверяет открыт ли фетчер."""
        return self._webdriver is not None

    def _add_headless_to_options(self) -> None:
        """Добавляет параметры драйверам для открытия браузера в тихом режиме."""

        options = self._webdriver_arguments.get("options")
        if options is None:
            if self._webdriver_class == FirefoxWebDriver:
                options = FirefoxOptions()
                options.add_argument("--headless")
            elif self._webdriver_class == ChromeWebDriver:
                options = ChromeOptions()
                options.add_argument("--headless")

        self._webdriver_arguments["options"] = options

    def _add_service_to_options(self) -> None:
        """Добавляет сервис для авто-установки драйверов."""

        service = self._webdriver_arguments.get("service")
        if service is None:
            if self._webdriver_class == FirefoxWebDriver:
                service = FirefoxService(GeckoDriverManager().install())
            elif self._webdriver_class == ChromeWebDriver:
                service = ChromeService(ChromeDriverManager().install())

        self._webdriver_arguments["service"] = service
