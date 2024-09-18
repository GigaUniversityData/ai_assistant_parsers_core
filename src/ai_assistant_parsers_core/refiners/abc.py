"""Абстракции для refiner'еров."""

import abc

from bs4 import BeautifulSoup


class ABCParsingRefiner(abc.ABC):
    """Базовый абстрактный refiner."""

    @abc.abstractmethod
    def refine(self, soup: BeautifulSoup) -> None:
        """Улучшает очищенный HTML-код после парсинга.

        Args:
            soup (BeautifulSoup): Объект beautiful soup.

        Returns:
            None: Улучшают HTML-код объекта ``soup``.
        """
