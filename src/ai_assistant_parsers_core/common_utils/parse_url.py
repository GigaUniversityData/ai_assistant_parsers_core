"""Утилиты для парсинга URL-адресов."""

from __future__ import annotations

from warnings import warn
from urllib.parse import urlparse, ParseResult

import tldextract
from tldextract.tldextract import ExtractResult


def parse_domain(url: str) -> ExtractResult:
    """Парсит домен и его элементы из URL-адреса.

    Args:
        url (str): URL-адрес.

    Returns:
        ExtractResult: Результат парсинга.
    """
    parsed_url = tldextract.extract(url)
    # subdomain = subdomain.replace("www.", "")
    return parsed_url


def parse_url(url: str) -> ParseResult:
    """Парсит URL-адрес.

    Args:
        url (str): URL-адрес.

    Returns:
        ParseResult: Результат парсинга.
    """
    return urlparse(url)


def normalize_url(url: str) -> str:
    """Нормализует URL-адрес так, чтобы одинаковые по сути URL-адреса,
    но разные по строке URL адреса в нормализации стали одинаковыми.

    Examples: 
        - ``https://spbu.ru/`` -> ``https://spbu.ru/``
        - ``https://spbu.ru``  -> ``https://spbu.ru/``

    Args:
        url (str): URL-адрес или URL-путь.

    Returns:
        str: URL-адрес или URL-путь.
    """
    if not url.endswith("/"):
        return f"{url}/"
    return url


def extract_url(url: str) -> ExtractResult:
    """Функция устарела. Пожалуйста, используйте вместо нее ``parse_domain``."""
    warn("The function is deprecated. Please use 'parse_domain' instead.", DeprecationWarning, stacklevel=2)
    return parse_domain(url)


def normalize_path(path: str) -> str:
    """Функция устарела. Пожалуйста, используйте вместо нее ``normalize_url``."""
    warn("The function is deprecated. Please use 'normalize_url' instead.", DeprecationWarning, stacklevel=2)
    return normalize_url(path)


def get_url_path(url: str) -> str:
    """Функция устарела. Пожалуйста, не используйте её."""
    warn("The function is deprecated. Please dont use this.", DeprecationWarning, stacklevel=2)
    return normalize_url(parse_url(url).path)
