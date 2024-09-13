"""Модуль для ``DomainMixin``."""

from __future__ import annotations

import re

from ai_assistant_parsers_core.common_utils.parse_url import get_url_subdomain, get_url_path


# TODO?: Убрать прикол в `www`
class DomainMixin():
    """
        Mixin для реализации метода ``check``, основываясь на поддомене.

        NOTE:
            Если необходимо парсить страницы сайта, которые не имеют поддомена, то следует передавать
            в аргументы ``supported_subdomains=["www"]``
    """

    def __init__(
        self,
        supported_subdomains: list[str],
        unsupported_paths: list[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        if unsupported_paths is None:
            unsupported_paths = []

        self._supported_subdomains = supported_subdomains
        self._unsupported_paths = unsupported_paths

    def check(self, url: str) -> bool:
        """Реализует метод ``check`` базового абстрактного класса."""

        subdomain = get_url_subdomain(url)
        path = get_url_path(url)

        return (
            subdomain in self._supported_subdomains
            and not self.__check_is_path_unsupported(path)
        )

    def __check_is_path_unsupported(self, path: str) -> bool:
        """Проверяет, поддерживается ли URL-путь.

        Args:
            path (str): URL-путь.

        Returns:
            bool: Булевый результат.
        """
        return any(
            re.fullmatch(pattern, path)
            for pattern in self._unsupported_paths
        )
