"""Команды ``parse_one``."""

from hashlib import md5
import importlib
import json
from pathlib import Path

import asyncclick as click
from bs4 import BeautifulSoup
from fake_headers import Headers
from ai_assistant_parsers_core.common_utils.parse_url import parse_domain
from ai_assistant_parsers_core.turn_html_into_markdown import turn_html_into_markdown
from ai_assistant_parsers_core.parsers import ABCParser
from ai_assistant_parsers_core.fetchers import AiohttpFetcher

from ai_assistant_parsers_core.cli.functions.parsing import parse_by_url, open_fetchers, close_fetchers


@click.command()
@click.argument("module_name", type=str)
@click.argument("output_dir", type=click.Path(path_type=Path))
@click.argument("url", type=str)
async def parse_one(module_name: str, output_dir: Path, url: str):
    """Парсит один URL-адрес, основываясь на конфигурации модуля.

    Пример ``settings.py`` со всеми параметрами:
    ```
    PARSERS = [WWWDomainParser(), UniversalParser()]

    # Опциональные
    PARSING_REFINERS = [CleanParsingRefiner(), RestructureParsingRefiner()]

    selenium_fetcher = SeleniumFetcher(webdriver.Firefox)
    FETCHERS_CONFIG = {
        "www.spbstu.ru/abit/master/to-choose-the-direction-of-training/education-program/": fetcher,
    }
    ```
    """

    output_dir.mkdir(exist_ok=True, parents=True)

    default_fetchers_config = {
        "*": AiohttpFetcher(dict(headers=Headers(os="mac", headers=True).generate())),
    }

    config = importlib.import_module(f"{module_name}.settings")
    parsers = config.PARSERS
    parsing_refiners = getattr(config, "PARSING_REFINERS", [])
    fetchers_config = getattr(config, "FETCHERS_CONFIG", {})
    fetchers_config = _merge_configs(default_fetchers_config, fetchers_config)

    await open_fetchers(fetchers_config=fetchers_config)

    # noinspection PyBroadException
    try:
        result = await parse_by_url(
            parsers=parsers,
            parsing_refiners=parsing_refiners,
            fetchers_config=fetchers_config,
            url=url,
        )
    except Exception as error:
        raise error
    else:
        _write_data_to_files(
            cleaned_soup=result.cleaned_html,
            url=url,
            parser=result.parser,
            output_dir=output_dir
        )
    finally:
        await close_fetchers(fetchers_config=fetchers_config)


def _merge_configs(default_fetchers_config: dict, fetchers_config: dict) -> dict:
    """Правильного объединяет параметров конфигов."""
    merged_config = fetchers_config.copy()
    for key, value in default_fetchers_config.items():
        if key not in merged_config:
            merged_config[key] = value
    return merged_config


def _write_data_to_files(cleaned_soup: BeautifulSoup, url: str, parser: ABCParser, output_dir: Path) -> None:
    """Записывает запаршенные данные в выходные файлы."""
    url_hash = f"{parse_domain(url).subdomain}_{_hash_string(url)}"
    parser_name = _get_full_parser_name(parser)
    html = str(cleaned_soup)

    result_dir = output_dir / url_hash
    result_dir.mkdir(exist_ok=True)

    click.echo(parser_name)

    path = result_dir / "result.html"
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(html)
    click.echo(f"file://{path.absolute()}")

    path = result_dir / "result.md"
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(turn_html_into_markdown(html))

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
