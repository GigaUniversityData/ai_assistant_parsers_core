"""Модуль для ``FindQueryMixin``."""

from __future__ import annotations

import typing as t

from bs4 import BeautifulSoup

from .base_query import BaseQueryMixin


class FindQueryMixin(BaseQueryMixin):
    """Mixin для реализации метода ``parse``, который оставляет только те HTML-блоки.
    HTML-блоки удаётся найти через ``soup.find``.
    """

    def __init__(self, find_arguments: list[dict[str, t.Any]], **kwargs) -> None:
        super().__init__(**kwargs)

        self._find_arguments = find_arguments

    def _prepare_result(self, source_html: BeautifulSoup, cleaned_html: BeautifulSoup) -> None:
        """Реализует метод ``_prepare_result`` базового абстрактного класса для метода ``source_html.find``."""

        assert cleaned_html.html is not None
        assert cleaned_html.html.body is not None

        for arguments in self._find_arguments:
            content = source_html.find(**arguments)

            if content is None:
                continue
            if content.name == "body":
                cleaned_html.html.body.decompose()
                cleaned_html.html.append(content)
                continue

            cleaned_html.html.body.append(content)
