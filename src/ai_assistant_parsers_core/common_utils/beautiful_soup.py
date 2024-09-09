from __future__ import annotations

import re
from urllib import parse

from bs4 import BeautifulSoup, Comment


# https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s08.html
URL_SCHEME_PATTERN = re.compile(r"^([a-z][a-z0-9+\-.]*):", re.IGNORECASE)


def clean_tags(soup: BeautifulSoup, tags: list[str]) -> None:
    for tag in soup.find_all(tags):
        tag.decompose()


def rewrite_urls(soup: BeautifulSoup, base_url: str | None = None) -> None:
    """Convert relative links to absolute URLs and unquote all."""

    if base_url and not re.match(r'^https?://', base_url):
        raise ValueError("Invalid base URL. It should start with http:// or https://")

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


def clean_comments(soup: BeautifulSoup) -> None:
    """Удаляет блоки коментариев."""
    comment: Comment
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()


def clean_empty_tags(soup: BeautifulSoup) -> None:
    """Удаляет все пустые теги (нет текста, дочерних тегов)."""
    for tag in soup.find_all():
        if not tag.text.strip():
            tag.decompose()
