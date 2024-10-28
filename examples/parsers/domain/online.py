"""
Страницы для теста:
- https://online.spbu.ru/nashi-kursy/
- https://online.spbu.ru/audiolekcii/
- https://online.spbu.ru/psixologiya-otdyxa/
- https://online.spbu.ru/leksikologiya-ispanskogo-yazyka/
"""

import re
from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.parse_url import get_url_path

from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select, clean_all_by_select


_MAIN_PATHS = [
    re.compile("/"),
    re.compile("/nashi-kursy/"),
    re.compile("/audiolekcii/"),
    re.compile("/novosti/"),
    re.compile("/resources/.*"),
    re.compile("/news/.*"),
    re.compile("/partners/"),
    re.compile("/o-centre/"),
    re.compile("/en/"),
    re.compile("/en/news/"),
    re.compile("/news_eng/.*"),
    re.compile("/en/courses/"),
    re.compile("/en/for-collaboration/"),
    re.compile("/cn/"),
]


class MainOnlineDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["online.spbu.ru"],
            select_arguments=["#main"],
        )

    def check(self, url: str) -> bool:
        return super().check(url) and any(regex.fullmatch(get_url_path(url)) for regex in _MAIN_PATHS)

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        clean_one_by_select(soup, "#header")
        clean_one_by_select(soup, ".close_news")

        # Особые страницы

        # https://online.spbu.ru/nashi-kursy
        clean_one_by_select(soup, "#searchform")
        # https://online.spbu.ru/coursera-announcement/
        clean_one_by_select(soup, ":has(> .language-switch__link)")
        # https://online.spbu.ru/o-centre/
        clean_one_by_select(soup, "#dm_embedded_58644")


class CourseOnlineDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["online.spbu.ru"],
            select_arguments=[".text"],
        )

    def check(self, url: str) -> bool:
        return super().check(url) and not any(regex.fullmatch(get_url_path(url)) for regex in _MAIN_PATHS)

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        clean_all_by_select(soup, ".clear")

        clean_one_by_select(soup, ".dop_links:has(> .items_kurs)")  # Рекомендуемые курсы
