from hashlib import md5
from aiohttp import ClientSession

from ai_assistant_parsers_core.parsers import ABCParser


def get_parser_by_url(url: str, parsers: list[ABCParser]) -> ABCParser:
    for parser in parsers:
        if parser.check(url=url):
            return parser
    raise RuntimeError


async def fetch_html_by_url(url: str, client: ClientSession) -> str:
    async with client.get(url) as response:
        try:
            return await response.text()
        except UnicodeDecodeError:
            return await response.text(encoding="windows-1251")


def get_full_parser_name(parser: ABCParser) -> str:
    return type(parser).__name__


def hash_string(string: str, size: int = 10) -> str:
    return md5(string.encode()).hexdigest()[:size]
