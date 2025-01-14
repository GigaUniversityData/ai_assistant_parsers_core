"""Модуль для запуска CLI-утилит."""

import asyncclick as click
from .commands import parse_one


COMMANDS = [parse_one]


@click.group()
def cli():
    """CLI утилиты для парсинга."""
    pass


if __name__ == "__main__":
    for command in COMMANDS:
        # noinspection PyTypeChecker
        cli.add_command(command)

    cli()
