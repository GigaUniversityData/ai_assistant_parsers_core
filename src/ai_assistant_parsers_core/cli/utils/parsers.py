from fnmatch import fnmatchcase
from hashlib import md5

from ai_assistant_parsers_core.parsers import ABCParser
from ai_assistant_parsers_core.fetchers import ABCFetcher
from ai_assistant_parsers_core.common_utils.parse_url import get_url_path


def get_parser_by_url(url: str, parsers: list[ABCParser]) -> ABCParser:
    for parser in parsers:
        if parser.check(url=url):
            return parser
    raise RuntimeError


async def fetch_html_by_url(url: str, config: dict[str, ABCFetcher], default_fetcher: ABCFetcher) -> str:
    for pattern, fetcher in config.items():
        url_path = get_url_path(url)
        if fnmatchcase(url_path, pattern):
            return await fetcher.fetch(url)

    return await default_fetcher.fetch(url)


def get_full_parser_name(parser: ABCParser) -> str:
    return type(parser).__name__


def hash_string(string: str, size: int = 10) -> str:
    return md5(string.encode()).hexdigest()[:size]
