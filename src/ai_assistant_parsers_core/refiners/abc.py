"""Абстракции для refiner'еров."""

import abc


class ABCParsingRefiner(abc.ABC):
    """Базовый абстрактный refiner."""

    @abc.abstractmethod
    def refine(self, html: str) -> str:
        """Улучшает очищенный HTML-код после парсинга.

        Args:
            html (str): HTML-код.

        Returns:
            str: Улучшенный HTML-код.
        """
