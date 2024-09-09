from __future__ import annotations

from bs4 import BeautifulSoup, Tag, NavigableString


def clean_one_by_find(soup: BeautifulSoup, args: dict):
    element = soup.find(**args)
    _clean_one_element(element)


def clean_one_by_select(soup: BeautifulSoup, selector: str):
    element = soup.select_one(selector)
    _clean_one_element(element)


def clean_all_by_find(soup: BeautifulSoup, args: dict) -> None:
    for element in soup.find_all(**args):
        _clean_one_element(element)


def clean_all_by_select(soup: BeautifulSoup, selector: str) -> None:
    for element in soup.select(selector):
        _clean_one_element(element)


def _clean_one_element(element: Tag | NavigableString | None) -> None:
    if element is None:
        return

    if isinstance(element, Tag):
        element.decompose()

    if isinstance(element, NavigableString):
        element.extract()
