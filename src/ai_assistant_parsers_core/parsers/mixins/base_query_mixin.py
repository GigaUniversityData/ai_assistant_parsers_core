"""Модуль для `BaseQueryMixin`."""

import abc
from bs4 import BeautifulSoup


class BaseQueryMixin(abc.ABC):
    """
    Базовый Mixin для простой реализации очистки HTML-кода. 
    Даёт возможность быстрой разработки парсеров.

    Методы, которые требуется реализовать:
        - `_prepare_result`

    Этапы (В порядке следования):
        1) `_clean_parsed_html` - Этап "CLEAR": Очистка лишних блоков из HTML-структуры.
        2) `_restructure_parsed_html` - Этап "RESTRUCTURED": Изменение структуры HTML кода для улучшения читаемости.
    """
    def parse(self, html: str) -> str:
        """Реализует метод `parse` базового абстрактного класса.

        Args:
            html (str): HTML-код.

        Returns:
            str: Очищенный HTML-код.
        """
        source_html = BeautifulSoup(html, "html5lib")
        cleaned_html = BeautifulSoup("<html><body></body></html>", "html.parser")

        self._prepare_result(source_html, cleaned_html)

        self._clean_parsed_html(cleaned_html)
        self._restructure_parsed_html(cleaned_html)

        return str(cleaned_html)

    @abc.abstractmethod
    def _prepare_result(self, source_html: BeautifulSoup, cleaned_html: BeautifulSoup) -> None:
        """Подготавливает и формирует результат `cleaned_html` основываясь на исходном `source_html`.

        Args:
            source_html (BeautifulSoup): Входной HTML-код.
            cleaned_html (BeautifulSoup): Очищенный HTML-код.
        """

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        """Очищает HTML-код.

        Args:
            soup (BeautifulSoup): HTML-код.
        """

    def _restructure_parsed_html(self, soup: BeautifulSoup) -> None:
        """Изменяет структуру HTML-кода для улучшения читаемости.

        Args:
            soup (BeautifulSoup): HTML-код.
        """
