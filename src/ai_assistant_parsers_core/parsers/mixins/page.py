"""Модуль для ``PageMixin``."""

from __future__ import annotations

from ai_assistant_parsers_core.common_utils.parse_url import get_url_path, parse_url


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

        self._allowed_paths = [path for path in allowed_paths]

        self.__check_allowed_paths()

    def check(self, url: str) -> bool:
        """Реализует метод ``check`` базового абстрактного класса."""
        url_path = f"{parse_url(url).netloc}{get_url_path(url)}"

        return url_path in self._allowed_paths

    def __check_allowed_paths(self):
        for path in self._allowed_paths:
            if not path.endswith("/"):
                raise ValueError(f"URL-путь {path} в 'allowed_paths' не корректен, используйте '{path}/'")
