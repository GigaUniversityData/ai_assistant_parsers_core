from __future__ import annotations

from bs4 import BeautifulSoup

from .base_query_mixin import BaseQueryMixin


class SimpleSelectMixin(BaseQueryMixin):
    def __init__(self, select_arguments: list[str], **kwargs) -> None:
        super().__init__(**kwargs)

        self._select_arguments = select_arguments

    def _prepare_result(self, soup: BeautifulSoup, result: BeautifulSoup) -> None:
        for arguments in self._select_arguments:
            content = soup.select_one(arguments)

            if content is None:
                continue
            if content.name == "body":
                result.html.body.decompose()
                result.html.append(content)
                continue

            result.html.body.append(content)
