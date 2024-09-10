"""Модуль для `UniversalParser`."""

from ai_assistant_parsers_core.common_utils.universal_clean_html import universal_clean_html

from ..abc import ABCParser


class UniversalParser(ABCParser):
    """
    Универсальный парсер, который может получить очищенный HTML-код из любого входного HTML.
    Рекомендуется только как временное решение, так как универсальные подходы работают не идеально.
    """

    def check(self, url: str) -> bool:
        return True

    def parse(self, html: str) -> str:
        return universal_clean_html(html)
