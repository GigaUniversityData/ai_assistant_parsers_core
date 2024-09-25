"""Модуль для ``SimpleFindDomainBaseParser``."""

from __future__ import annotations

import typing as t

from ..abc import ABCParser
from ..mixins import DomainMixin, FindQueryMixin


class SimpleFindDomainBaseParser(DomainMixin, FindQueryMixin, ABCParser):
    """
    Базовый класс, который просто совмещает в себе Mixin'ы ``DomainMixin`` и ``FindQueryMixin``.

    NOTE:
        Читайте описания соответствующих Mixin'ов для изучения их работы.
    """

    def __init__(
        self,
        allowed_domains_paths: list[str],
        find_arguments: list[dict[str, t.Any]],
        excluded_paths: list[str] | None = None,
        included_paths: list[str] | None = None,
    ) -> None:
        super().__init__(
            allowed_domains_paths=allowed_domains_paths,
            excluded_paths=excluded_paths,
            included_paths=included_paths,
            find_arguments=find_arguments,
        )
