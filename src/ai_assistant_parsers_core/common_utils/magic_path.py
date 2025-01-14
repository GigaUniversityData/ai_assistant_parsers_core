import typing as t
import re
from fnmatch import fnmatchcase
from functools import cached_property

from ai_assistant_parsers_core.common_utils.parse_url import normalize_url, parse_url, parse_domain


class MagicURL:
    def __init__(self, url: str) -> None:
        self._url = url
        self._parsed_url = parse_url(url)
        self._parsed_domain = parse_domain(url)

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
    def domain_name(self):
        return self._parsed_domain.domain

    @property
    def domain_subdomain(self):
        return self._parsed_domain.subdomain

    @property
    def domain_suffix(self):
        return self._parsed_domain.suffix

    @cached_property
    def normalized_url(self):
        return normalize_url(self.url)

    @cached_property
    def normalized_path(self):
        return normalize_url(self.path)

    def is_path_regex_match(self, pattern: str | re.Pattern[str]) -> bool:
        return re.match(pattern, self.normalized_path) is not None

    def is_path_fn_match(self, pattern: t.AnyStr) -> bool:
        return fnmatchcase(self.normalized_path, pattern)

    def is_path_equals(self, string: str) -> bool:
        return string == self.normalized_path
