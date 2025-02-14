"""Модуль для ``DefaultRefiner``."""

import re
from bs4 import BeautifulSoup, Tag

from ai_assistant_parsers_core.common_utils.beautiful_soup import (
    clean_comments,
    URL_SCHEME_PATTERN,
    converts_relative_links_to_absolute,
    clean_tags,
)

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

    def refine(self, soup: BeautifulSoup, url: str) -> None:
        """Реализует метод ``refine`` базового абстрактного класса."""
        self._clear(soup, url)
        self._restructure(soup, url)

    def _clear(self, soup, url: str) -> None:
        # Лишние HTML-теги
        clean_tags(soup, ["img"])
        #clean_tags(soup, ["aside"])

        # Теги не влияющие на контент
        clean_tags(soup, ["script", "style", "noscript"])
        clean_comments(soup)
        #clean_empty_tags(soup)

        # Мелкий остаток, не влияющий на отображение
        _clear_javascript_scheme_from_links(soup)

    def _restructure(self, soup, url: str) -> None:
        converts_relative_links_to_absolute(soup, base_url=url)

    def __patch_html_for_markdown_converter(self, soup: BeautifulSoup) -> None:
        """Патчит HTML для преобразователя HTML в Markdown."""
        _clean_empty_style_tags(soup)
        _clean_empty_list_items(soup)
        _clean_all_excess_tags_from_links(soup)


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
