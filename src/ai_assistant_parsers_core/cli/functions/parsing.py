"""Служебные функции для парсинга."""

from fnmatch import fnmatchcase
from dataclasses import dataclass

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.parse_url import parse_url, normalize_path
from ai_assistant_parsers_core.parsers import ABCParser
from ai_assistant_parsers_core.refiners import ABCParsingRefiner
from ai_assistant_parsers_core.fetchers import ABCFetcher


@dataclass
class ParsingResult:
    """Результат парсинга."""
    raw_html: BeautifulSoup
    cleaned_html: BeautifulSoup
    parser: ABCParser


async def parse_by_url(
    parsers: list[ABCParser],
    parsing_refiners: list[ABCParsingRefiner],
    fetchers_config: dict[str, ABCFetcher],
    default_fetcher: ABCFetcher,
    url: str,
) -> ParsingResult:
    """Парсит по URL-адресу.

    Args:
        parsers (list[ABCParser]): Список парсеров.
        parsing_refiners (list[ABCParsingRefiner]): Список рефайнеров парсеров.
        fetchers_config (dict[str, ABCFetcher]): Конфиг для фетчеров
        default_fetcher (ABCFetcher): Фетчер по умолчанию.
        url (str): URL-адрес для парсинга.

    Returns:
        ParsingResult: Результат парсинга.
    """
    html = await fetch_html_by_url(url, fetchers_config=fetchers_config, default_fetcher=default_fetcher)

    raw_soup = BeautifulSoup(html, "html5lib")

    parser = get_parser_by_url(url, parsers=parsers)
    cleaned_soup = process_parsed_html(parser=parser, parsing_refiners=parsing_refiners, url=url, raw_soup=raw_soup)

    return ParsingResult(raw_html=raw_soup, cleaned_html=cleaned_soup, parser=parser)


def process_parsed_html(
    parser: ABCParser,
    parsing_refiners: list[ABCParsingRefiner],
    url: str,
    raw_soup: BeautifulSoup,
) -> BeautifulSoup:
    """Обрабатывает сырой HTML.

    Args:
        parser (ABCParser): Парсер.
        parsing_refiners (list[ABCParsingRefiner]): Список рефайнеров парсеров.
        url (str): URL-адрес.
        raw_soup (BeautifulSoup): Сырой HTML.

    Returns:
        BeautifulSoup: Очищенный HTML.
    """
    try:
        cleaned_soup = parser.parse(raw_soup, url=url)
    except Exception as error:
        raise ParsingError(url=url, parser=parser, html=str(raw_soup)) from error

    for parsing_refiner in parsing_refiners:
        try:
            parsing_refiner.refine(cleaned_soup, url=url)
        except Exception as error:
            raise RefineError(url=url, refiner=parsing_refiner, html=str(cleaned_soup)) from error

    return cleaned_soup


async def open_fetchers(default_fetcher: ABCFetcher, fetchers_config: dict[str, ABCFetcher]) -> None:
    """Отрывает все фетчеры.

    Args:
        default_fetcher (ABCFetcher): Фетчер по-умолчанию.
        fetchers_config (dict[str, ABCFetcher]): Конфиг фетчеров.
    """
    await default_fetcher.open()
    for _, fetcher in fetchers_config.items():
        if not fetcher.is_open():
            await fetcher.open()


async def close_fetchers(default_fetcher: ABCFetcher, fetchers_config: dict[str, ABCFetcher]) -> None:
    """Закрывает все фетчеры.

    Args:
        default_fetcher (ABCFetcher): Фетчер по-умолчанию.
        fetchers_config (dict[str, ABCFetcher]): Конфиг фетчеров.
    """
    await default_fetcher.close()
    for _, fetcher in fetchers_config.items():
        if fetcher.is_open():
            await fetcher.close()


async def fetch_html_by_url(url: str, fetchers_config: dict[str, ABCFetcher], default_fetcher: ABCFetcher) -> str:
    """Извлекает HTML по URL-адресу.

    Args:
        url (str): URL-адрес.
        fetchers_config (dict[str, ABCFetcher]): Конфиг фетчеров.
        default_fetcher (ABCFetcher): Фетчер по-умолчанию.

    Returns:
        str: Извлечённый HTML-код.
    """
    for pattern, fetcher in fetchers_config.items():
        parsed_url = parse_url(url)
        check_path = normalize_path(f"{parsed_url.netloc}{parsed_url.path}")
        if fnmatchcase(check_path, pattern):
            try:
                return await fetcher.fetch(url)
            except Exception as error:
                raise FetchingError(url=url, fetcher=fetcher) from error

    return await default_fetcher.fetch(url)


def get_parser_by_url(url: str, parsers: list[ABCParser]) -> ABCParser:
    """Получает подходящий парсер для данного URL-адреса по данному URL-адресу.

    Args:
        url (str): URL-адрес
        parsers (list[ABCParser]): Список парсеров.

    Raises:
        RuntimeError: Если необходимого парсера для данного URL-адреса не существует.

    Returns:
        ABCParser: Парсер.
    """
    for parser in parsers:
        if parser.check(url=url):
            return parser
    raise RuntimeError("Required parser for this URL does not exist")


class BaseParsingError(Exception):
    pass


class FetchingError(BaseParsingError):
    def __init__(self, url: str, fetcher: ABCFetcher):
        self.url = url
        self.fetcher = fetcher

    def __str__(self):
        return f"Error when fetching {self.url} by {self.fetcher}"


class RefineError(BaseParsingError):
    def __init__(self, url: str, refiner: ABCParsingRefiner, html: str):
        self.url = url
        self.refiner = refiner
        self.html = html

    def __str__(self):
        return f"Error when refine with {self.url} by {self.refiner}"


class ParsingError(BaseParsingError):
    def __init__(self, url: str, parser: ABCParser, html: str):
        self.url = url
        self.parser = parser
        self.html = html

    def __str__(self):
        return f"Error when parsing with {self.url} by {self.parser}"
