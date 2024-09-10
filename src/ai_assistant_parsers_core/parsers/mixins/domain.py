"""Модуль для `DomainMixin`."""

from __future__ import annotations

import re

from ai_assistant_parsers_core.common_utils.parse_url import get_url_subdomain, get_url_path


class DomainMixin():
    """Mixin для реализации метода `check`, основываясь на поддомене."""

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
        """Реализует метод `check` базового абстрактного класса.

        Args:
            url (str): URL-адрес.

        Returns:
            bool: Булевый результат.
        """

        subdomain = get_url_subdomain(url)
        path = get_url_path(url)

        return (
            subdomain in self._supported_subdomains
            and not self.__check_is_path_unsupported(path)
        )

    def __check_is_path_unsupported(self, path: str) -> bool:
        return any(
            re.fullmatch(pattern, path)
            for pattern in self._unsupported_paths
        )
