from hashlib import md5
import importlib
import json
from pathlib import Path

import asyncclick as click
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from fake_headers import Headers
from ai_assistant_parsers_core.common_utils.parse_url import extract_url
from ai_assistant_parsers_core.turn_html_into_markdown import turn_html_into_markdown
from ai_assistant_parsers_core.parsers import ABCParser
from ai_assistant_parsers_core.fetchers import AiohttpFetcher

from ai_assistant_parsers_core.cli.functions.parsing import parse_by_url, open_fetchers, close_fetchers


@click.command()
@click.argument("module_name", type=str)
@click.argument("output_dir", type=click.Path(path_type=Path))
@click.argument("url", type=str)
async def parse_one(module_name: str, output_dir: Path, url: str):
    output_dir.mkdir(exist_ok=True, parents=True)

    config = importlib.import_module(f"{module_name}.settings")
    default_fetcher = AiohttpFetcher(dict(headers=Headers(os="mac", headers=True).generate()))
    parsers = config.PARSERS
    parsing_refiners = getattr(config, "PARSING_REFINERS", [])
    fetchers_config = getattr(config, "FETCHERS_CONFIG", {})

    await open_fetchers(default_fetcher=default_fetcher, fetchers_config=fetchers_config)

    result = await parse_by_url(
        parsers=parsers,
        parsing_refiners=parsing_refiners,
        fetchers_config=fetchers_config,
        default_fetcher=default_fetcher,
        url=url,
    )

    await close_fetchers(default_fetcher=default_fetcher, fetchers_config=fetchers_config)
    _write_data_to_files(
        cleaned_soup=result.cleaned_html,
        url=url,
        parser=result.parser,
        output_dir=output_dir
    )


def _write_data_to_files(cleaned_soup: BeautifulSoup, url: str, parser: ABCParser, output_dir: Path) -> None:
    url_hash = f"{extract_url(url).subdomain}_{_hash_string(url)}"
    parser_name = _get_full_parser_name(parser)
    html = str(cleaned_soup)

    result_dir = output_dir / url_hash
    result_dir.mkdir(exist_ok=True)

    click.echo(parser_name)

    path = result_dir / "result.html"
    with open(path, "w") as fp:
        fp.write(html)
    click.echo(f"file://{path.absolute()}")

    path = result_dir / "result.md"
    with open(path, "w") as fp:
        fp.write(turn_html_into_markdown(html))

    click.echo(f"file://{path.absolute()}")

    metadata = {"parser_name": parser_name, "url": url, "hash": url_hash}
    path = result_dir / "meta.json"
    with open(path, "w") as fp:
        json.dump(metadata, fp=fp, indent=4)


def _get_full_parser_name(parser: ABCParser) -> str:
    return type(parser).__name__


def _hash_string(string: str, size: int = 10) -> str:
    return md5(string.encode()).hexdigest()[:size]
