"""Команды ``parse_one``."""

import importlib
import json
from hashlib import md5
from pathlib import Path

import asyncclick as click
from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.beautiful_soup import add_base_tag
from ai_assistant_parsers_core.common_utils.parse_url import parse_domain
from ai_assistant_parsers_core.markdown_converter import convert_html_to_markdown
from ai_assistant_parsers_core.parsers import ABCParser
from ai_assistant_parsers_core.fetchers import APIFetcher
from ai_assistant_parsers_core.cli.functions.parsing import parse_by_url, open_fetchers, close_fetchers, ParsingResult


@click.command()
@click.argument("module_name", type=str)
@click.argument("output_dir", type=click.Path(path_type=Path))
@click.argument("url", type=str)
async def parse_one(module_name: str, output_dir: Path, url: str) -> None:
    """Парсит один URL-адрес, основываясь на конфигурации модуля.

    Пример ``settings.py`` со всеми параметрами:

    .. code-block:: python

        PARSERS = [WWWDomainParser(), UniversalParser()]

        # Опциональные
        PARSING_REFINERS = [CleanParsingRefiner(), RestructureParsingRefiner()]
    """

    output_dir.mkdir(exist_ok=True, parents=True)

    default_fetchers_config = {"*": APIFetcher()}

    config = importlib.import_module(f"{module_name}.settings")
    parsers = config.PARSERS
    parsing_refiners = getattr(config, "PARSING_REFINERS", [])

    await open_fetchers(fetchers_config=default_fetchers_config)

    # noinspection PyBroadException
    try:
        parsing_result = await parse_by_url(
            parsers=parsers,
            parsing_refiners=parsing_refiners,
            fetchers_config=default_fetchers_config,
            url=url,
        )
    except Exception as error:
        raise error
    else:
        await _write_data_to_files(parsing_result=parsing_result, output_dir=output_dir)
    finally:
        await close_fetchers(fetchers_config=default_fetchers_config)


async def _write_data_to_files(
    parsing_result: ParsingResult,
    output_dir: Path,
) -> None:
    """Записывает запаршенные данные в выходные файлы."""
    url = parsing_result.url
    parser = parsing_result.parser
    cleaned_soup = parsing_result.cleaned_soup
    raw_soup = parsing_result.raw_soup

    url_hash = f"{parse_domain(url).subdomain}_{_hash_string(url)}"
    parser_name = _get_full_parser_name(parser)
    cleaned_html = str(cleaned_soup)

    result_dir = output_dir / url_hash
    result_dir.mkdir(exist_ok=True)

    click.echo(parser_name)

    path = result_dir / "input.html"
    add_base_tag(raw_soup, base_url=url)
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(str(raw_soup))
    click.echo(f"file://{path.absolute()}")

    path = result_dir / "result.html"
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(str(cleaned_soup))
    click.echo(f"file://{path.absolute()}")

    path = result_dir / "result.md"
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(await convert_html_to_markdown(cleaned_html))

    click.echo(f"file://{path.absolute()}")

    metadata = {"parser_name": parser_name, "url": url, "hash": url_hash}
    path = result_dir / "meta.json"
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(metadata, fp=fp, indent=4)


def _get_full_parser_name(parser: ABCParser) -> str:
    """Получает полное имя парсера."""
    return type(parser).__name__


def _hash_string(string: str, size: int = 10) -> str:
    """Хеширует строку."""
    return md5(string.encode()).hexdigest()[:size]
