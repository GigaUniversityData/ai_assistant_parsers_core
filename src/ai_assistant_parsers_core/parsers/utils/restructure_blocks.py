"""
Утилиты для изменения структуры HTML-кода.
Как правило, нужны для улучшения читаемости HTML-кода.
"""

from __future__ import annotations

from functools import partial

from bs4 import BeautifulSoup, Tag


def rename_all_by_select(soup: BeautifulSoup | Tag, selector: str, replace_name: str) -> None:
    """Меняет имя всем HTML-тегам на заданное по селектору для ``soup.select``.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        selector (str): CSS-селектор для ``soup.select``.
        replace_name (str): Имя для замены.
    """
    for tag in soup.select(selector):
        _rename_one_element(tag, replace_name=replace_name)


def rename_one_by_select(soup: BeautifulSoup | Tag, selector: str, replace_name: str) -> None:
    """Меняет имя одному HTML-тегу на заданное по селектору для ``soup.select_one``.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        selector (str): CSS-селектор для ``soup.select_one``.
        replace_name (str): Имя для замены.
    """
    tag = soup.select_one(selector)
    _rename_one_element(tag, replace_name=replace_name)


html = partial(BeautifulSoup, features="html.parser")


def _rename_one_element(tag: Tag | None, replace_name: str) -> None:
    if tag is None:
        return

    if isinstance(tag, Tag):
        tag.name = replace_name
