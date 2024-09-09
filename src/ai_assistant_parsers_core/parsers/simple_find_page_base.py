from __future__ import annotations

import typing as t

from .abc import ABCParser
from .mixins import SimpleFindMixin


class SimpleFindPageBaseParser(SimpleFindMixin, ABCParser):
    def __init__(
        self,
        supported_urls: list[str],
        find_arguments: list[dict[str, t.Any]],
    ) -> None:
        super().__init__(find_arguments=find_arguments)

        self._supported_urls = supported_urls

    def check(self, url: str) -> bool:
        return url in self._supported_urls
