"""Модуль для ``SelectQueryMixin``."""

from __future__ import annotations

from bs4 import BeautifulSoup

from .base_query import BaseQueryMixin


class SelectQueryMixin(BaseQueryMixin):
    """Mixin для реализации метода ``parse``, который оставляет только те HTML-блоки.
    HTML-блоки удаётся найти через ``soup.select_one``.
    """

    def __init__(self, select_arguments: list[str], **kwargs) -> None:
        super().__init__(**kwargs)

        self._select_arguments = select_arguments

    def _prepare_result(self, source_html: BeautifulSoup, cleaned_html: BeautifulSoup) -> None:
        """Реализует метод ``_prepare_result`` базового абстрактного класса для метода ``source_html.select_one``."""

        assert cleaned_html.html is not None
        assert cleaned_html.html.body is not None

        for arguments in self._select_arguments:
            content = source_html.select_one(arguments)

            if content is None:
                continue
            if content.name == "body":
                cleaned_html.html.body.decompose()
                cleaned_html.html.append(content)
                continue

            cleaned_html.html.body.append(content)
