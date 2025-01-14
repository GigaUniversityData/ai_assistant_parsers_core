"""Абстракции для парсеров."""

import abc

from bs4 import BeautifulSoup


from ai_assistant_parsers_core.magic_url import MagicURL


class ABCParser(abc.ABC):
    """Базовый абстрактный парсер."""

    @abc.abstractmethod
    def check(self, magic_url: MagicURL) -> bool:
        """Проверяет URL-адрес, чтобы убедиться, что он подходит для парсинга.

        Args:
            magic_url (MagicURL): Волшебный объект обёртывающий URL-адрес страницы.

        Returns:
            bool: Булевый результат.
        """

    @abc.abstractmethod
    def parse(self, soup: BeautifulSoup, magic_url: MagicURL) -> BeautifulSoup:
        """Парсит HTML-код, чтобы получить очищенный HTML-код.

        Args:
            soup (BeautifulSoup): Объект beautiful soup.
            magic_url (MagicURL): Волшебный объект обёртывающий URL-адрес страницы.

        Returns:
            BeautifulSoup: Очищенный HTML-код (Другой объект `BeautifulSoup`).
        """
