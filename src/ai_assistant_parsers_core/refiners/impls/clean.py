"""Модуль для ``CleanPostParsingRefiner``."""

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.beautiful_soup import clean_comments, URL_SCHEME_PATTERN
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_all_by_select

from ..abc import ABCParsingRefiner


class CleanParsingRefiner(ABCParsingRefiner):
    """Производит универсальную очистку "очищенного HTML-кода"."""

    def refine(self, soup: BeautifulSoup) -> str:
        """Реализует метод ``refine`` базового абстрактного класса."""

        for tag in ["script", "style", "noscript"]:
            clean_all_by_select(soup, tag)

        #clean_tags(soup, ["aside"])
        clean_comments(soup)
        #clean_empty_tags(soup)
        #clean_tags(soup, ["clear", "cls"])
        _clear_javascript_scheme_from_links(soup)

        return str(soup)


def _clear_javascript_scheme_from_links(soup: BeautifulSoup) -> None:
    """
    Очищает javascript схему в URL-адресах.

    Пример страницы: https://artesliberales.spbu.ru/ru/faculty
    """
    tag = "a"
    attr = "href"
    for element in soup.find_all(tag, **{attr: True}):
        url = element.get(attr, "").strip()
        if not url:
            continue

        match = URL_SCHEME_PATTERN.match(url)
        if match is None:
            continue

        if match.group(1) == "javascript":
            del element[attr]
