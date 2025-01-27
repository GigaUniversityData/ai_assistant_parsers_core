"""Утилиты для парсинга URL-адресов."""

from __future__ import annotations

from urllib.parse import urlparse, ParseResult

from typing_extensions import deprecated
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


@deprecated("Please use 'parse_domain' instead")
def extract_url(url: str) -> ExtractResult:
    return parse_domain(url)


@deprecated("Please use 'normalize_url' instead")
def normalize_path(path: str) -> str:
    return normalize_url(path)


@deprecated("Please don't use this")
def get_url_path(url: str) -> str:
    return normalize_url(parse_url(url).path)
