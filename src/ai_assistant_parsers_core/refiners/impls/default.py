"""Модуль для ``DefaultRefiner``."""

import re
from bs4 import BeautifulSoup, Tag

from ai_assistant_parsers_core.common_utils.beautiful_soup import (
    clean_comments,
    URL_SCHEME_PATTERN,
    converts_relative_links_to_absolute,
)
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_all_by_select
from ai_assistant_parsers_core.magic_url import MagicURL

from ..abc import ABCParsingRefiner


STYLE_TAGS_REGEX = re.compile(r"""
^(?:
    h[1-6]         # Заголовки h1-h6
    | strong       # Жирный текст (строгий)
    | b            # Жирный текст
    | i            # Курсив
    | em           # Выделение (обычно курсив)
    | mark         # Выделение маркером
    | small        # Мелкий текст
    | del          # Удаленный текст
    | ins          # Вставленный текст
    | sub          # Нижний индекс
    | sup          # Верхний индекс
    | u            # Невыраженная аннотация (Волнистое подчеркивание).
)$
""", flags=re.VERBOSE)


class DefaultRefiner(ABCParsingRefiner):
    """Производит универсальную очистку "очищенного HTML-кода" и
    производит изменение структуры "очищенного HTML-кода" для улучшения его читаемости.
    """

    def refine(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        """Реализует метод ``refine`` базового абстрактного класса."""
        self._clear(soup, magic_url)
        self._restructure(soup, magic_url)

    def _clear(self, soup, magic_url: MagicURL) -> None:
        for tag in ["script", "style", "noscript"]:
            clean_all_by_select(soup, tag)

        # clean_tags(soup, ["aside"])
        # clean_empty_tags(soup)
        clean_comments(soup)
        _clear_javascript_scheme_from_links(soup)
        _clean_empty_style_tags(soup)
        _clean_empty_list_items(soup)
        _clean_all_excess_tags_from_links(soup)

    def _restructure(self, soup, magic_url: MagicURL) -> None:
        converts_relative_links_to_absolute(soup, base_url=magic_url.url)


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


def _clean_empty_style_tags(soup: BeautifulSoup) -> None:
    """Очищает пустые HTML-теги стиля (``h1``, ``b``, ``i``, ``em`` и тп.).

    Args:
        soup (BeautifulSoup): Объект beautiful soup.
    """
    style_tags = soup.find_all(STYLE_TAGS_REGEX)
    for tag in style_tags.copy():
        content = _get_tag_text_without_spaces(tag)
        if not content:
            tag.decompose()


def _clean_empty_list_items(soup: BeautifulSoup) -> None:
    """Очищает пустые ``li`` HTML-теги.

    Args:
        soup (BeautifulSoup): Объект beautiful soup.
    """
    tags = soup.find_all("li")
    for tag in tags.copy():
        content = _get_tag_text_without_spaces(tag)
        if not content:
            tag.decompose()


def _get_tag_text_without_spaces(tag: Tag) -> str:
    """Получает из объекта тега текст без пробелов.

    Args:
        tag (Tag): Объект тега.

    Returns:
        str: Текст.
    """
    return re.sub(r"\s", "", tag.get_text())


def _clean_all_excess_tags_from_links(soup: BeautifulSoup):
    for link in soup.select("a"):
        for attr_key in tuple(link.attrs.keys()):
            if attr_key == "href":
                continue
            del link[attr_key]
