"""Абстракции для парсеров."""

import abc

from bs4 import BeautifulSoup


from ai_assistant_parsers_core.common_utils.magic_path import MagicPath


class ABCParser(abc.ABC):
    """Базовый абстрактный парсер."""

    @abc.abstractmethod
    def check(self, path: MagicPath) -> bool:
        """Проверяет URL-адрес, чтобы убедиться, что он подходит для парсинга.

        Args:
            path (MagicPath): Волшебный объект обёртывающий URL-адрес страницы.

        Returns:
            bool: Булевый результат.
        """

    @abc.abstractmethod
    def parse(self, soup: BeautifulSoup, path: MagicPath) -> BeautifulSoup:
        """Парсит HTML-код, чтобы получить очищенный HTML-код.

        Args:
            soup (BeautifulSoup): Объект beautiful soup.
            path (MagicPath): Волшебный объект обёртывающий URL-адрес страницы.

        Returns:
            BeautifulSoup: Очищенный HTML-код (Другой объект `BeautifulSoup`).
        """
