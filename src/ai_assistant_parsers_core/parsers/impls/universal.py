"""Модуль для ``UniversalParser``."""
from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.universal_clean_html import universal_clean_html
from ai_assistant_parsers_core.common_utils.magic_path import MagicPath

from ..abc import ABCParser


class UniversalParser(ABCParser):
    """
    Универсальный парсер, который может получить очищенный HTML-код из любого входного HTML.
    Рекомендуется только как временное решение, так как универсальные подходы работают не идеально.
    """

    def check(self, path: MagicPath) -> bool:
        """Реализует метод ``check`` базового абстрактного класса."""

        return True

    def parse(self, soup: BeautifulSoup, path: MagicPath) -> BeautifulSoup:
        """Реализует метод ``parse`` базового абстрактного класса."""

        return universal_clean_html(soup)
