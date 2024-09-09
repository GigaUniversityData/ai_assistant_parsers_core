from __future__ import annotations

from .abc import ABCParser
from .mixins import SimpleSelectMixin


class SimpleFindPageBaseParser(SimpleSelectMixin, ABCParser):
    def __init__(
        self,
        supported_urls: list[str],
        select_arguments: list[str],
    ) -> None:
        super().__init__(select_arguments=select_arguments)

        self._supported_urls = supported_urls

    def check(self, url: str) -> bool:
        return url in self._supported_urls
