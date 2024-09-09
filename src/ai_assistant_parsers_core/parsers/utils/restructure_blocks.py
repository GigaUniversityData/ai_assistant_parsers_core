from __future__ import annotations

from bs4 import BeautifulSoup, Tag


def rename_all_by_select(soup: BeautifulSoup, selector: str, replace_name: str) -> None:
    for tag in soup.select(selector):
        _raname_element(tag, replace_name=replace_name)


def rename_one_by_select(soup: BeautifulSoup, selector: str, replace_name: str) -> None:
    tag = soup.select_one(selector)
    _raname_element(tag, replace_name=replace_name)


# TODO: Это работает с html5lib, но релевантно ли это?
def convert_tables_to_divs(soup: BeautifulSoup):
    rename_all_by_select(soup, "table", replace_name="div")


def _raname_element(tag: Tag | None, replace_name: str) -> None:
    if tag is None:
        return

    if isinstance(tag, Tag):
        tag.name = replace_name
