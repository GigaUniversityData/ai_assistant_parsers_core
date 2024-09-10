from __future__ import annotations

from ..abc import ABCParser
from ..mixins import PageMixin, SelectQueryMixin


class SimpleFindPageBaseParser(PageMixin, SelectQueryMixin, ABCParser):
    def __init__(
        self,
        supported_urls: list[str],
        select_arguments: list[str],
    ) -> None:
        super().__init__(select_arguments=select_arguments, supported_urls=supported_urls)
