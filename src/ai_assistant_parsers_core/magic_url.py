"""Модуль для ``MagicURL``."""

import typing as t
import re
from fnmatch import fnmatchcase
from functools import cached_property
from pathlib import PurePosixPath, PurePath

from ai_assistant_parsers_core.common_utils.parse_url import normalize_url, parse_url, parse_domain


class MagicURL:
    """Класс для разбора URL и предоставления доступа к его компонентам."""

    def __init__(self, url: str) -> None:
        self._url = url
        self._parsed_url = parse_url(url)
        self._parsed_domain = parse_domain(url)

    @property
    def magic_path(self) -> PurePath:
        """Возвращает путь URL в виде объекта ``pathlib``."""
        return PurePosixPath(self.path)

    @property
    def url(self) -> str:
        """Возвращает исходный URL."""
        return self._url

    @property
    def scheme(self) -> str:
        """Возвращает схему URL."""
        return self._parsed_url.scheme

    @property
    def netloc(self) -> str:
        """Возвращает сетевое расположение URL."""
        return self._parsed_url.netloc

    @property
    def path(self) -> str:
        """Возвращает путь URL."""
        return self._parsed_url.path

    @property
    def query(self) -> str:
        """Возвращает строку запроса URL."""
        return self._parsed_url.query

    @property
    def params(self) -> str:
        """Возвращает параметры URL."""
        return self._parsed_url.params

    @property
    def fragment(self) -> str:
        """Возвращает фрагмент URL."""
        return self._parsed_url.fragment

    @cached_property
    def normalized_url(self) -> str:
        """Возвращает нормализованный URL."""
        return normalize_url(self.url)

    @cached_property
    def normalized_path(self) -> str:
        """Возвращает нормализованный путь URL."""
        return normalize_url(self.path)

    @property
    def domain_name(self) -> str:
        """Возвращает основное имя доменной части."""
        return self._parsed_domain.domain

    @property
    def domain_subdomain(self) -> str:
        """Возвращает субдомен доменной части."""
        return self._parsed_domain.subdomain

    @property
    def domain_suffix(self) -> str:
        """Возвращает суффикс (TLD) доменной части."""
        return self._parsed_domain.suffix

    def is_path_regex_match(self, pattern: str | re.Pattern[str]) -> bool:
        """Проверяет, соответствует ли нормализованный путь заданному регулярному выражению.

        Args:
            pattern (str | re.Pattern): Шаблон регулярного выражения.

        Returns:
            bool: True, если совпадает, иначе False.
        """
        return re.match(pattern, self.normalized_path) is not None

    def is_path_fn_match(self, pattern: t.AnyStr) -> bool:
        """Проверяет, соответствует ли нормализованный путь заданному шаблону fnmatch.

        Args:
            pattern (str | bytes): Шаблон fnmatch.

        Returns:
            bool: True, если совпадает, иначе False.
        """
        return fnmatchcase(self.normalized_path, pattern)

    def is_path_equals(self, string: str) -> bool:
        """
        Проверяет, равен ли нормализованный путь заданной строке.

        Args:
            string (str): Строка для сравнения.

        Returns:
            bool: True, если равен, иначе False.
        """
        return string == self.normalized_path
