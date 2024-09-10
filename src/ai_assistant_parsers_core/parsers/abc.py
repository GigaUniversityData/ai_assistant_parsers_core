"""Абстракции для парсеров."""

import abc


class ABCParser(abc.ABC):
    """Базовый абстрактный парсер."""

    @abc.abstractmethod
    def check(self, url: str) -> bool:
        """Проверяет URL-адрес, чтобы убедиться, что он подходит для парсинга.

        Args:
            url (str): URL-адрес.

        Returns:
            bool: Булевый результат.
        """

    @abc.abstractmethod
    def parse(self, html: str) -> str:
        """Парсит HTML-код, чтобы получить очищенный HTML-код.

        Args:
            html (str): HTML-код.

        Returns:
            str: Очищенный HTML-код.
        """
