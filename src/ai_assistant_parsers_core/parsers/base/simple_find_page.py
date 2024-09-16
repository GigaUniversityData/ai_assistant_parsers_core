"""Модуль для ``SimpleFindPageBaseParser``."""

from __future__ import annotations

import typing as t

from ..abc import ABCParser
from ..mixins import PageMixin, FindQueryMixin


class SimpleFindPageBaseParser(PageMixin, FindQueryMixin, ABCParser):
    """
    Базовый класс, который просто совмещает в себе Mixin'ы ``PageMixin`` и ``FindQueryMixin``.

    NOTE:
        Читайте описания соответствующих Mixin'ов для изучения их работы.
    """

    def __init__(
        self,
        allowed_paths: list[str],
        find_arguments: list[dict[str, t.Any]],
    ) -> None:
        super().__init__(find_arguments=find_arguments, allowed_paths=allowed_paths)
