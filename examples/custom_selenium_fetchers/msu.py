"""
Фетчер для сайта ``https://msu.ru/*``

реализует ожидание загрузки класса ``page`` перед началом сбора данных.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ai_assistant_parsers_core.fetchers import SeleniumFetcher


class CustomSeleniumFetcher(SeleniumFetcher):
    def after_getting_page(self) -> None:
        try:
            WebDriverWait(self._webdriver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "page")
                ),
            )
        finally:
            pass
