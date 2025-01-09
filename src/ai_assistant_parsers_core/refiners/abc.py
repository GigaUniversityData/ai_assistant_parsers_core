"""Абстракции для refiner'еров."""

import abc

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.magic_path import MagicPath


class ABCParsingRefiner(abc.ABC):
    """Базовый абстрактный refiner."""

    @abc.abstractmethod
    def refine(self, soup: BeautifulSoup, path: MagicPath) -> None:
        """Улучшает очищенный HTML-код после парсинга.

        Args:
            soup (BeautifulSoup): Объект beautiful soup.
            path (MagicPath): Волшебный объект обёртывающий URL-адрес страницы.

        Returns:
            None: Улучшают HTML-код объекта ``soup``.
        """
