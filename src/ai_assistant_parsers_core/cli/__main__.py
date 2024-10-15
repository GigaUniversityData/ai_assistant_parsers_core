import click
from .commands import parse_one


COMMANDS = [parse_one]


@click.group()
def cli():
    pass


for command in COMMANDS:
    cli.add_command(command)


if __name__ == "__main__":
    cli()
