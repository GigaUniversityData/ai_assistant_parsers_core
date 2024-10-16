import asyncclick as click
from .commands import parse_one


COMMANDS = [parse_one]


@click.group()
def cli():
    pass


if __name__ == "__main__":
    for command in COMMANDS:
        cli.add_command(command)

    cli()
