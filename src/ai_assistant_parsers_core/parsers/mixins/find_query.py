from __future__ import annotations

import typing as t

from bs4 import BeautifulSoup

from .base_query_mixin import BaseQueryMixin


class FindQueryMixin(BaseQueryMixin):
    def __init__(self, find_arguments: list[dict[str, t.Any]], **kwargs) -> None:
        super().__init__(**kwargs)

        self._find_arguments = find_arguments

    def _prepare_result(self, soup: BeautifulSoup, result: BeautifulSoup) -> None:
        for arguments in self._find_arguments:
            content = soup.find(**arguments)

            if content is None:
                continue
            if content.name == "body":
                result.html.body.decompose()
                result.html.append(content)
                continue

            result.html.body.append(content)
