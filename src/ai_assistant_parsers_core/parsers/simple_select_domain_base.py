from __future__ import annotations

from .abc import ABCParser
from .mixins import SimpleDomainMixin, SimpleSelectMixin


class SimpleSelectDomainBaseParser(SimpleDomainMixin, SimpleSelectMixin, ABCParser):
    def __init__(
        self,
        supported_subdomains: list[str], 
        select_arguments: list[str],
        unsupported_paths: list[str] | None = None,
    ) -> None:
        super().__init__(
            supported_subdomains=supported_subdomains,
            unsupported_paths=unsupported_paths,
            select_arguments=select_arguments,
        )
