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
        allowed_domains_paths: list[str],
        select_arguments: list[str],
        excluded_paths: list[str] | None = None,
        included_paths: list[str] | None = None,
    ) -> None:
        super().__init__(
            allowed_domains_paths=allowed_domains_paths,
            excluded_paths=excluded_paths,
            included_paths=included_paths,
            select_arguments=select_arguments,
        )
