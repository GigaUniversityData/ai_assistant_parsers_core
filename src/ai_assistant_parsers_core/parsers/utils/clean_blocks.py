"""Утилиты для очистки HTML-блоков."""

from __future__ import annotations

import typing as t

from bs4 import BeautifulSoup, Tag, NavigableString


def clean_one_by_find(soup: BeautifulSoup | Tag, args: dict[str, t.Any]):
    """Очищает один HTML-блок по аргументам через ``soup.find``.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        args (dict[str, t.Any]): Словарь аргументов для ``soup.find``.
    """
    element = soup.find(**args)
    _clean_one_element(element)


def clean_one_by_select(soup: BeautifulSoup | Tag, selector: str):
    """Очищает один HTML-блок по селектору через ``soup.select_one``.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        selector (str): CSS-селектор для ``soup.select_one``.
    """
    element = soup.select_one(selector)
    _clean_one_element(element)


def clean_all_by_find(soup: BeautifulSoup | Tag, args: dict[str, t.Any]) -> None:
    """Очищает все HTML-блоки по аргументам через ``soup.find_all``.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        args (dict[str, t.Any]): Словарь аргументов для ``soup.find_all``.
    """
    for element in soup.find_all(**args):
        _clean_one_element(element)


def clean_all_by_select(soup: BeautifulSoup | Tag, selector: str) -> None:
    """Очищает все HTML-блоки по селектору через ``soup.select``.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        selector (str): CSS-селектор для ``soup.select``.
    """
    for element in soup.select(selector):
        _clean_one_element(element)


def _clean_one_element(element: Tag | NavigableString | None) -> None:
    if element is None:
        return

    if isinstance(element, Tag):
        element.decompose()

    if isinstance(element, NavigableString):
        element.extract()
