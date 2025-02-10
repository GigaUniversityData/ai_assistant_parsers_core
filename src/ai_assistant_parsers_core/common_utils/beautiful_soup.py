"""Утилиты для работы с BeautifulSoup."""

from __future__ import annotations

import re
from urllib import parse

from bs4 import BeautifulSoup, Tag, Comment


URL_SCHEME_PATTERN = re.compile(r"^([a-z][a-z0-9+\-.]*):", re.IGNORECASE)
"""Паттерн для извлечения ``scheme`` из URL адреса. 

Смотри: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s08.html
"""


def clean_tags(soup: BeautifulSoup | Tag, tags: list[str]) -> None:
    """Очищает теги из списка по названию.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        tags (list[str]): Список тегов.
    """

    for tag in soup.find_all(tags):
        tag.decompose()


def converts_relative_links_to_absolute(soup: BeautifulSoup | Tag, base_url: str | None = None) -> None:
    """Преобразует относительные ссылки в абсолютные ссылки и их декодирует.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
        base_url (str | None, optional): Базовый URL-адрес. По умолчанию None.
    """

    tags_to_process = [
        ("a", "href"),
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
    ]

    for tag, attr in tags_to_process:
        for element in soup.find_all(tag, **{attr: True}):
            url = element.get(attr, "").strip()
            if not url:
                continue

            if base_url:
                if not URL_SCHEME_PATTERN.match(url):
                    element[attr] = parse.unquote(parse.urljoin(base_url, url))
                else:
                    element[attr] = parse.unquote(url)
            else:
                element[attr] = parse.unquote(url)


def clean_comments(soup: BeautifulSoup | Tag) -> None:
    """Удаляет блоки комментариев.

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
    """

    comment: Comment
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()


def clean_empty_tags(soup: BeautifulSoup | Tag) -> None:
    """Удаляет все пустые теги (нет текста, нет дочерних тегов).

    Args:
        soup (BeautifulSoup | Tag): Объект beautiful soup.
    """
    for tag in soup.find_all():
        if not tag.text.strip():
            tag.decompose()
