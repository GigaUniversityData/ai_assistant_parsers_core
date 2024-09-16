"""Модуль для ``SimpleFindPageBaseParser``."""

from __future__ import annotations

from ..abc import ABCParser
from ..mixins import PageMixin, SelectQueryMixin


class SimpleSelectPageBaseParser(PageMixin, SelectQueryMixin, ABCParser):
    """
    Базовый класс, который просто совмещает в себе Mixin'ы ``PageMixin`` и ``SelectQueryMixin``.

    NOTE:
        Читайте описания соответствующих Mixin'ов для изучения их работы.
    """

    def __init__(
        self,
        allowed_paths: list[str],
        select_arguments: list[str],
    ) -> None:
        super().__init__(select_arguments=select_arguments, allowed_paths=allowed_paths)
