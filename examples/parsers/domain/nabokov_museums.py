from bs4 import BeautifulSoup

from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select, clean_all_by_select
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser


class NabokovMuseumsDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["nabokov.museums.spbu.ru"],
            select_arguments=["#main"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        clean_one_by_select(soup, ".footer-logo")
        clean_one_by_select(soup, ".social_bottom_block")

        # Блок "Другие события"
        clean_all_by_select(soup, ".another-events-title + .row")
        clean_one_by_select(soup, ".another-events-title")
