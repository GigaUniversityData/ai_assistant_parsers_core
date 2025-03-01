"""
Страницы для теста:
- https://nabokov.museums.spbu.ru/ru/ekskursii.html
- https://nabokov.museums.spbu.ru/ru/nauchnye-issledovaniya.html
"""

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.magic_url import MagicURL
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select, clean_all_by_select


class NabokovMuseumsDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["nabokov.museums.spbu.ru"],
            select_arguments=["#main"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        clean_one_by_select(soup, ".footer-logo")
        clean_one_by_select(soup, ".social_bottom_block")

        # Блок "Другие события"
        clean_all_by_select(soup, ".another-events-title + .row")
        clean_one_by_select(soup, ".another-events-title")
