import typing as t
import re
from fnmatch import fnmatchcase

from ai_assistant_parsers_core.common_utils.parse_url import normalize_path, parse_url, extract_path


class MagicPath:
    def __init__(self, url: str) -> None:
        self._url = url
        self._parsed_url = parse_url(url)
        self._extracted_path = extract_path(url)

    @property
    def url(self):
        return self._url

    @property
    def scheme(self):
        return self._parsed_url.scheme

    @property
    def netloc(self):
        return self._parsed_url.netloc

    @property
    def path(self):
        return self._parsed_url.path

    @property
    def query(self):
        return self._parsed_url.query

    @property
    def params(self):
        return self._parsed_url.params

    @property
    def fragment(self):
        return self._parsed_url.fragment

    @property
    def path_domain(self):
        return self._extracted_path.domain

    @property
    def path_subdomain(self):
        return self._extracted_path.subdomain

    @property
    def path_suffix(self):
        return self._extracted_path.suffix

    @property
    def normalized_url(self):
        return normalize_path(self.url)

    @property
    def normalized_path(self):
        return normalize_path(self.path)

    def is_path_regex_match(self, pattern: str | re.Pattern[str]) -> bool:
        return re.match(pattern, self.normalized_path) is not None

    def is_path_fn_match(self, pattern: t.AnyStr) -> bool:
        return fnmatchcase(self.normalized_path, pattern)

    def is_path_equals(self, string: str) -> bool:
        return string == self.normalized_path
