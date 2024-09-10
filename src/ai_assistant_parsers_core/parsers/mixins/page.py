"""Модуль для `PageMixin`."""

from __future__ import annotations


class PageMixin():
    """Mixin для реализации метода `check`, основываясь на URL-адресах страниц."""

    def __init__(
        self,
        supported_urls: list[str],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self._supported_urls = supported_urls

    def check(self, url: str) -> bool:
        """Реализует метод `check` базового абстрактного класса.

        Args:
            url (str): URL-адрес.

        Returns:
            bool: Булевый результат.
        """

        return url in self._supported_urls
