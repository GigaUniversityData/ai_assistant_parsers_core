"""
Страницы для теста:
- https://pr.spbu.ru/smi
- https://pr.spbu.ru/social-network
"""

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.magic_url import MagicURL
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select


class PRDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["pr.spbu.ru"],
            select_arguments=[".main-block"]
        )

    def _clean_parsed_html(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        clean_one_by_select(soup, 'section:has(> .g-container > h1:-soup-contains-own("Напишите нам"))')
