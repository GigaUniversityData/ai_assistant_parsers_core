from __future__ import annotations

import typing as t

from ..abc import ABCParser
from ..mixins import DomainMixin, FindQueryMixin


class SimpleFindDomainBaseParser(DomainMixin, FindQueryMixin, ABCParser):
    def __init__(
        self,
        supported_subdomains: list[str],
        find_arguments: list[dict[str, t.Any]],
        unsupported_paths: list[str] | None = None,
    ) -> None:
        super().__init__(
            supported_subdomains=supported_subdomains,
            unsupported_paths=unsupported_paths,
            find_arguments=find_arguments,
        )
