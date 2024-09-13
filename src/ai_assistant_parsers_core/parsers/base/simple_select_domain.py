"""Модуль для ``SimpleSelectDomainBaseParser``."""

from __future__ import annotations

from ..abc import ABCParser
from ..mixins import DomainMixin, SelectQueryMixin


class SimpleSelectDomainBaseParser(DomainMixin, SelectQueryMixin, ABCParser):
    """
    Базовый класс, который просто совмещает в себе Mixin'ы ``DomainMixin`` и ``SelectQueryMixin``.

    NOTE:
        Читайте описания соответствующих Mixin'ов для изучения их работы.
    """

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
