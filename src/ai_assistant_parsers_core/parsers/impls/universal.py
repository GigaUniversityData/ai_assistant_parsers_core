from ai_assistant_parsers_core.common_utils.universal_clean_html import universal_clean_html

from ..abc import ABCParser


class UniversalParser(ABCParser):
    def check(self, url: str) -> bool:
        return True

    def parse(self, html: str) -> str:
        return universal_clean_html(html)
