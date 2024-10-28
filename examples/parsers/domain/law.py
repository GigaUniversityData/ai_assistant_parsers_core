"""
Страницы для теста:
- https://law.spbu.ru/science/
- https://law.spbu.ru/pregraduatestudy/
"""

from bs4 import BeautifulSoup, Tag

from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser


class LawDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["law.spbu.ru"],
            select_arguments=["body"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        body: Tag = soup.find(name="body")  # type: ignore

        for child in body.contents.copy():
            if isinstance(child, Tag) and child.name != "section":
                child.decompose()

        clean_one_by_select(soup, "section.breadcrumbs")

        clean_one_by_select(soup, ".submenu")
        clean_one_by_select(soup, ".submenu-second")

        # Особые страницы #

        # /aboutfaculty/teachers/*
        clean_one_by_select(soup, ".otherlecturer-")
        clean_one_by_select(soup, ":has(> .slider-main-news-thumbs)")
