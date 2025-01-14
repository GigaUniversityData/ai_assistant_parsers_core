"""Утилиты для парсинга URL-адресов."""

from __future__ import annotations

from urllib.parse import urlparse, ParseResult

import tldextract
from tldextract.tldextract import ExtractResult


def parse_domain(url: str) -> ExtractResult:
    """Получает поддомен из URL-адреса.

    Args:
        url (str): URL-адрес.

    Returns:
        str: Поддомен.
    """
    parsed_url = tldextract.extract(url)
    # subdomain = subdomain.replace("www.", "")
    return parsed_url


def parse_url(url: str) -> ParseResult:
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


def get_normalized_path(url: str) -> str:
    """Извлекает и нормализует путь из заданного URL-адреса.

    Examples:
        - ``https://spbu.ru/`` -> ``spbu.ru/``

    Args:
        url (str): URL-адрес.

    Returns:
        str: URL-путь.
    """
    return normalize_url(parse_url(url).path)
