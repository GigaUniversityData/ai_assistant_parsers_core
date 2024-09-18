from bs4 import BeautifulSoup

from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select
from ai_assistant_parsers_core.parsers import SimpleSelectPageBaseParser


class AbiturientMainPageParser(SimpleSelectPageBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_paths=["abiturient.spbu.ru/"],
            select_arguments=["main"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        clean_one_by_select(soup, ".news")
        clean_one_by_select(soup, ".news.news--events")
        clean_one_by_select(soup, ".footnote.footer-note")
