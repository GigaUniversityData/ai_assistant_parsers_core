from __future__ import annotations

from urllib.parse import urlparse

import tldextract


def get_url_subdomain(url: str) -> str:
    parsed_url = tldextract.extract(url)
    subdomain = parsed_url.subdomain
    subdomain = subdomain.replace("www.", "")
    subdomain = subdomain if subdomain else "www"
    return subdomain


def get_url_path(url: str) -> str:
    return normalize_path(urlparse(url).path)


def normalize_path(path: str) -> str:
    if not path.endswith("/"):
        return f"{path}/"
    return path
