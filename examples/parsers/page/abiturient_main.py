from bs4 import BeautifulSoup

from ai_assistant_parsers_core.magic_url import MagicURL
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select


class AbiturientMainPageParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["abiturient.spbu.ru"],
            included_paths=["/"],
            select_arguments=["main"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        clean_one_by_select(soup, ".news")
        clean_one_by_select(soup, ".news.news--events")
        clean_one_by_select(soup, ".footnote.footer-note")
