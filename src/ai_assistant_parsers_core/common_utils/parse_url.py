"""Утилиты для парсинга URL-адресов."""

from __future__ import annotations

from urllib.parse import urlparse, ParseResult

import tldextract
from tldextract.tldextract import ExtractResult


def extract_path(url: str) -> ExtractResult:
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


def get_url_path(url: str) -> str:
    """Получает URL-путь из URL-адреса.

    Examples:
        - ``https://spbu.ru/`` -> ``spbu.ru/``

    Args:
        url (str): URL-адрес.

    Returns:
        str: URL-путь.
    """
    return normalize_path(parse_url(url).path)


def normalize_path(path: str) -> str:
    """Нормализует URL-адрес так, чтобы одинаковые по суте URL-адреса, но разные по строке URL адреса в нормализации стали одинаковыми.

    Examples: 
        - ``https://spbu.ru/`` -> ``https://spbu.ru/``
        - ``https://spbu.ru``  -> ``https://spbu.ru/``

    Args:
        path (str): URL-адрес или URL-путь.

    Returns:
        str: URL-адрес или URL-путь.
    """

    if not path.endswith("/"):
        return f"{path}/"
    return path
