"""Утилита для универсальной очистки любого HTML-кода."""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from ai_assistant_parsers_core.common_utils.beautiful_soup import clean_tags, clean_comments


def universal_clean_html(soup: BeautifulSoup) -> BeautifulSoup:
    """Очищает HTML-код.

    Args:
        soup (BeautifulSoup): Объект beautiful soup.

    Returns:
        str: HTML-код.
    """

    for tag in ["body", "main"]:
        found_tag = soup.find(tag)

        if isinstance(found_tag, Tag):
            soup = found_tag


    clean_tags(soup, ["script", "style", "noscript", "nav", "head", "footer", "header"])
    #_clean_specific_css(soup)
    clean_comments(soup)
    #clean_empty_tags(soup)

    # Очитка атрибутов
    _clean_attributes(soup)

    soup.name = "html"

    return soup


def _clean_specific_css(soup: BeautifulSoup | Tag) -> None:
    """Удаляет теги по специальным селекторам.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
    """

    for tag in soup.select('div[id*="google-cache-hdr"], div[id*="wm-ipp"], div[class*="bread"], ul[class*="bread"], div[class*="menu"], li[class*="menu"], section[class*="anchors"]'):
        tag.decompose()


def _clean_attributes(soup: BeautifulSoup | Tag) -> None:
    """Удаляет ненужные атрибуты тегам.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
    """
    tag: Tag

    for tag in soup.find_all(True):  # True finds all tags
        attrs_to_remove = [attr for attr in tag.attrs if attr not in ["text", "src", "href"]]
        for attr in attrs_to_remove:
            del tag[attr]
