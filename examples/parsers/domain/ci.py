"""
Страницы для теста:
- https://ci.spbu.ru/
- https://ci.spbu.ru/category/svedenia_o_kitae/confucius/
"""

import re

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_find, clean_one_by_select
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser


class CIDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["ci.spbu.ru"],
            select_arguments=[".pad.group"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        # Блок "Статьи по теме..."
        clean_one_by_select(soup, ".heading:has(> .fa.fa-hand-o-right)")
        clean_one_by_select(soup, ".related-posts")

        # Счётчик просмотров
        clean_one_by_find(soup, dict(string=re.compile(r"Просмотров: [\d ]+")))
