import importlib
import json
from pathlib import Path

import asyncclick as click
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from fake_headers import Headers
from ai_assistant_parsers_core.common_utils.beautiful_soup import converts_relative_links_to_absolute
from ai_assistant_parsers_core.common_utils.parse_url import extract_url
from ai_assistant_parsers_core.turn_html_into_markdown import turn_html_into_markdown
from ai_assistant_parsers_core.parsers import ABCParser
from ai_assistant_parsers_core.refiners import ABCParsingRefiner
from ai_assistant_parsers_core.fetchers import ABCFetcher, AiohttpFetcher

from ai_assistant_parsers_core.cli.utils.parsers import (
    get_parser_by_url,
    hash_string,
    get_full_parser_name,
    fetch_html_by_url,
)


@click.command()
@click.argument("module_name", type=str)
@click.argument("output_dir", type=click.Path(path_type=Path))
@click.argument("url", type=str)
async def parse_one(module_name: str, output_dir: Path, url: str):
    output_dir.mkdir(exist_ok=True, parents=True)

    module = importlib.import_module(f"{module_name}.settings")
    parsers = module.PARSERS
    parsing_refiners = getattr(module, "PARSING_REFINERS", [])
    fetchers_config = getattr(module, "FETCHERS", {})
    default_fetcher = AiohttpFetcher(
        client=ClientSession(headers=Headers(os="mac", headers=True).generate()),
    )

    await _process_url(
        output_dir=output_dir,
        parsers=parsers,
        parsing_refiners=parsing_refiners,
        fetchers_config=fetchers_config,
        default_fetcher=default_fetcher,
        url=url,
    )


async def _process_url(
    output_dir: Path,
    parsers: list[ABCParser],
    parsing_refiners: list[ABCParsingRefiner],
    fetchers_config: dict[str, ABCFetcher],
    default_fetcher: ABCFetcher,
    url: str,
) -> None:
    html = await fetch_html_by_url(url, config=fetchers_config, default_fetcher=default_fetcher)
    soup = BeautifulSoup(html, "html5lib")
    parser = get_parser_by_url(url, parsers=parsers)

    cleaned_soup = _process_html(parser=parser, parsing_refiners=parsing_refiners, url=url, soup=soup)
    _write_data_to_files(cleaned_soup=cleaned_soup, url=url, parser=parser, output_dir=output_dir)
    await _close_fetchers(default_fetcher=default_fetcher, fetchers_config=fetchers_config)


def _process_html(
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


def _write_data_to_files(cleaned_soup: BeautifulSoup, url: str, parser: ABCParser, output_dir: Path) -> None:
    url_hash = f"{extract_url(url).subdomain}_{hash_string(url)}"
    parser_name = get_full_parser_name(parser)
    html = str(cleaned_soup)

    result_dir = output_dir / url_hash
    result_dir.mkdir(exist_ok=True)

    print(parser_name)

    path = result_dir / "result.html"
    with open(path, "w") as fp:
        fp.write(html)
    print(f"file://{path.absolute()}")

    path = result_dir / "result.md"
    with open(path, "w") as fp:
        fp.write(turn_html_into_markdown(html))

    print(f"file://{path.absolute()}")

    metadata = {"parser_name": parser_name, "url": url, "hash": url_hash}
    path = result_dir / "meta.json"
    with open(path, "w") as fp:
        json.dump(metadata, fp=fp, indent=4)


async def _close_fetchers(default_fetcher: ABCFetcher, fetchers_config: dict[str, ABCFetcher]) -> None:
    await default_fetcher.close()
    for _, fetcher in fetchers_config.items():
        await fetcher.close()
