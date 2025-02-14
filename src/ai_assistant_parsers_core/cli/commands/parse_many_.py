"""Команды ``parse_many``."""

import sys
from pathlib import Path

import asyncclick as click
from .parse_one_ import parse_one


@click.command()
@click.argument("module_name", type=str)
@click.argument("output_dir", type=click.Path(path_type=Path))
async def parse_many(module_name: str, output_dir: Path) -> None:
    """Парсит множество URL-адресов, основываясь на конфигурации модуля."""
    input_ = sys.stdin.read().strip()
    urls = input_.split()
    for index, url in enumerate(urls, start=1):
        click.echo(click.style(f"{index}. {url}", fg="green", bold=True))
        await parse_one.callback(module_name, output_dir, url)
