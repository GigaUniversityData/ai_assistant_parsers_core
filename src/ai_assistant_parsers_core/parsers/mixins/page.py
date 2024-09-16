"""Модуль для ``PageMixin``."""

from __future__ import annotations

from ai_assistant_parsers_core.common_utils.parse_url import get_url_path, normalize_path


class PageMixin():
    """
    Mixin для реализации метода ``check``, основываясь на URL-адресах страниц.

    Examples:
        - Правильно: ``PageMixin(allowed_paths=["spbu.ru/education/"])``
        - Не правильно: ``PageMixin(allowed_paths=["spbu.ru/education"])``
    """

    def __init__(
        self,
        allowed_paths: list[str],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self._allowed_paths = [normalize_path(path) for path in allowed_paths]

    def check(self, url: str) -> bool:
        """Реализует метод ``check`` базового абстрактного класса."""
        url_path = get_url_path(url)

        return url_path in self._allowed_paths
