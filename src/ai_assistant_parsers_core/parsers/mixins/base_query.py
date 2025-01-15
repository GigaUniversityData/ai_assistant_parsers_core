"""Модуль для ``BaseQueryMixin``."""
from __future__ import annotations

import typing as t
import inspect
import abc

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.magic_url import MagicURL


class BaseQueryMixin(abc.ABC):
    """
    Базовый Mixin для простой реализации очистки HTML-кода. 
    Даёт возможность быстрой разработки парсеров.

    Методы, которые требуется реализовать:
        - ``_prepare_result``

    Опциональные методы (В порядке выполнения):
        1) ``_clean_parsed_html`` - Этап "CLEAR": Очистка лишних блоков из HTML-структуры.
        2) ``_restructure_parsed_html`` - Этап "RESTRUCTURED": Изменение структуры HTML кода для улучшения читаемости.

    NOTE:
        С точки зрения кода методы ``_clean_parsed_html`` и ``_restructure_parsed_html`` ничем не различаются
        и ничего не делают. Их работа зависит лишь от того, как их реализовать.
    """

    def parse(self, soup: BeautifulSoup, magic_url: MagicURL) -> BeautifulSoup:
        """Реализует метод ``parse`` базового абстрактного класса."""
        source_html = soup
        cleaned_html = BeautifulSoup("<html><head></head><body></body></html>", "html5lib")

        self._prepare_result(source_html, cleaned_html)

        self.__call_function_with_optional_parameters(self._clean_parsed_html, cleaned_html, magic_url=magic_url)
        self.__call_function_with_optional_parameters(self._restructure_parsed_html, cleaned_html, magic_url=magic_url)

        return cleaned_html

    @abc.abstractmethod
    def _prepare_result(self, source_html: BeautifulSoup, cleaned_html: BeautifulSoup) -> None:
        """Подготавливает и формирует результат ``cleaned_html`` основываясь на исходном ``source_html``.

        Args:
            source_html (BeautifulSoup): Входной HTML-код.
            cleaned_html (BeautifulSoup): Очищенный HTML-код.
        """

    def _clean_parsed_html(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        """
        Метод для реализации.

        Этот метод может быть переопределен в дочерних классах для
        добавления специфической функциональности. По умолчанию не выполняет никаких действий.

        Служит для очистки HTML-кода.

        Args:
            soup (BeautifulSoup): Объект beautiful soup.
            magic_url (MagicURL): Волшебный объект обёртывающий URL-адрес страницы.
        """

    def _restructure_parsed_html(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        """
        Метод для реализации.

        Этот метод может быть переопределен в дочерних классах для
        добавления специфической функциональности. По умолчанию не выполняет никаких действий.

        Служит для изменения структуры HTML-кода для улучшения читаемости.

        Args:
            soup (BeautifulSoup): HTML-код.
            magic_url (MagicURL): Волшебный объект обёртывающий URL-адрес страницы.
        """

    def __call_function_with_optional_parameters(
        self,
        function: t.Callable,
        cleaned_html: BeautifulSoup,
        magic_url: MagicURL,
    ) -> None:
        signature = inspect.signature(function)

        # TODO: Deprecated
        if "magic_url" not in signature.parameters:
            function(cleaned_html)
            return

        function(cleaned_html, magic_url=magic_url)
