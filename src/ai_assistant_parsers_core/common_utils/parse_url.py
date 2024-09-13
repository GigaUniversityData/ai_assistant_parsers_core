"""Утилиты для парсинга URL-адресов."""

from __future__ import annotations

from urllib.parse import urlparse

import tldextract


def get_url_subdomain(url: str) -> str:
    """Получает поддомен из URL-адреса.

    Args:
        url (str): URL-адрес.

    Returns:
        str: Поддомен.
    """
    parsed_url = tldextract.extract(url)
    subdomain = parsed_url.subdomain
    subdomain = subdomain.replace("www.", "")
    subdomain = subdomain if subdomain else "www"
    return subdomain


def get_url_path(url: str) -> str:
    """Получает URL-путь из URL-адреса.

    Examples:
        - ``https://spbu.ru/`` -> ``spbu.ru/``

    Args:
        url (str): URL-адрес.

    Returns:
        str: URL-путь.
    """
    return normalize_path(urlparse(url).path)


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
