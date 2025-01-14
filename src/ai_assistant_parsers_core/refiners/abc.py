"""Абстракции для refiner'еров."""

import abc

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.magic_url import MagicURL


class ABCParsingRefiner(abc.ABC):
    """Базовый абстрактный refiner."""

    @abc.abstractmethod
    def refine(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        """Улучшает очищенный HTML-код после парсинга.

        Args:
            soup (BeautifulSoup): Объект beautiful soup.
            magic_url (MagicURL): Волшебный объект обёртывающий URL-адрес страницы.

        Returns:
            None: Улучшают HTML-код объекта ``soup``.
        """
