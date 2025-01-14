"""Модуль для ``DomainMixin``."""

from __future__ import annotations

from fnmatch import fnmatchcase

from ai_assistant_parsers_core.common_utils.parse_url import get_normalized_path, parse_url
from ai_assistant_parsers_core.common_utils.magic_path import MagicURL


class DomainMixin:
    # noinspection GrazieInspection
    """Mixin для реализации метода ``check``, основываясь на поддомене.

        Examples:
            - ``DomainMixin(allowed_domains_paths=["spbu.ru"], excluded_paths=["/virtual_tour/*"])``
            - ``DomainMixin(allowed_domains_paths=["spbu.ru"], excluded_paths=["/component/users/*?"])``
            - Правильно: ``DomainMixin(allowed_domains_paths=["pr.spbu.ru"], excluded_paths=["/museum/web-sites/"])``
            - Не правильно: ``DomainMixin(allowed_domains_paths=["pr.spbu.ru/"], excluded_paths=["/museum/web-sites"])``

        NOTE:
            Шаблоны для ``excluded_paths``:

            ==========  ========
            Шаблон      Значение
            ==========  ========
            ``*``       Соответствует всему
            ``?``       Соответствует любому отдельному символу
            ``[seq]``   Соответствует любому символу в ``seq``
            ``[!seq]``  Соответствует любому символу, не входящему в ``seq``
            ==========  ========
    """

    def __init__(
        self,
        allowed_domains_paths: list[str],
        excluded_paths: list[str] | None = None,
        included_paths: list[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        if excluded_paths is None:
            excluded_paths = []

        self._allowed_domains_paths = allowed_domains_paths
        self._excluded_paths = excluded_paths
        self._included_paths = included_paths

    def check(self, magic_url: MagicURL) -> bool:
        """Реализует метод ``check`` базового абстрактного класса."""
        domain_path = parse_url(magic_url.url).netloc
        url_path = get_normalized_path(magic_url.url)

        return (
            domain_path in self._allowed_domains_paths
            and not self.__check_is_path_excluded(url_path)
            and self.__check_is_path_included(url_path)
        )

    def __check_is_path_excluded(self, path: str) -> bool:
        """Проверяет, поддерживается ли URL-путь.

        Args:
            path (str): URL-путь.

        Returns:
            bool: Булевый результат.
        """
        return any(
            fnmatchcase(path, pattern)
            for pattern in self._excluded_paths
        )

    def __check_is_path_included(self, path: str) -> bool:
        """Проверяет, поддерживается ли URL-путь.

        Args:
            path (str): URL-путь.

        Returns:
            bool: Булевый результат.
        """
        if self._included_paths is None:
            return True

        return any(
            fnmatchcase(path, pattern)
            for pattern in self._included_paths
        )
