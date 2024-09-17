"""Абстракции для парсеров."""

import abc

from bs4 import BeautifulSoup


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
    def parse(self, soup: BeautifulSoup) -> str:
        """Парсит HTML-код, чтобы получить очищенный HTML-код.

        Args:
            soup (BeautifulSoup): Объект beautiful soup.

        Returns:
            str: Очищенный HTML-код.
        """
