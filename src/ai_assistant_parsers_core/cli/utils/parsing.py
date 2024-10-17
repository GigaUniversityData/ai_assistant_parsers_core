from fnmatch import fnmatchcase

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.parse_url import get_url_path
from ai_assistant_parsers_core.common_utils.beautiful_soup import converts_relative_links_to_absolute
from ai_assistant_parsers_core.parsers import ABCParser
from ai_assistant_parsers_core.refiners import ABCParsingRefiner
from ai_assistant_parsers_core.fetchers import ABCFetcher


async def process_url(
    parsers: list[ABCParser],
    parsing_refiners: list[ABCParsingRefiner],
    fetchers_config: dict[str, ABCFetcher],
    default_fetcher: ABCFetcher,
    url: str,
) -> tuple[BeautifulSoup, ABCParser]:
    html = await fetch_html_by_url(url, fetchers_config=fetchers_config, default_fetcher=default_fetcher)

    soup = BeautifulSoup(html, "html5lib")

    parser = get_parser_by_url(url, parsers=parsers)
    cleaned_soup = process_html(parser=parser, parsing_refiners=parsing_refiners, url=url, soup=soup)

    return cleaned_soup, parser


def process_html(
    parser: ABCParser,
    parsing_refiners: list[ABCParsingRefiner],
    url: str,
    soup: BeautifulSoup,
) -> BeautifulSoup:
    cleaned_soup = parser.parse(soup)
    converts_relative_links_to_absolute(soup=cleaned_soup, base_url=url)
    for parsing_refiner in parsing_refiners:
        parsing_refiner.refine(cleaned_soup)

    return cleaned_soup


async def open_fetchers(default_fetcher: ABCFetcher, fetchers_config: dict[str, ABCFetcher]) -> None:
    await default_fetcher.open()
    for _, fetcher in fetchers_config.items():
        await fetcher.open()


async def close_fetchers(default_fetcher: ABCFetcher, fetchers_config: dict[str, ABCFetcher]) -> None:
    await default_fetcher.close()
    for _, fetcher in fetchers_config.items():
        await fetcher.close()


async def fetch_html_by_url(url: str, fetchers_config: dict[str, ABCFetcher], default_fetcher: ABCFetcher) -> str:
    for pattern, fetcher in fetchers_config.items():
        url_path = get_url_path(url)
        if fnmatchcase(url_path, pattern):
            return await fetcher.fetch(url)

    return await default_fetcher.fetch(url)


def get_parser_by_url(url: str, parsers: list[ABCParser]) -> ABCParser:
    for parser in parsers:
        if parser.check(url=url):
            return parser
    raise RuntimeError
