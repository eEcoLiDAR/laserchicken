"""Command line tool definitions."""
from __future__ import print_function

import click
from colorama import Back, init

from . import ToolException
from .._version import __version__
from .io import _load, _save


@click.group()
@click.version_option(version=__version__)
def main():
    """Define top level tool."""


@main.command(name='import', help='Convert .las file to .ply file.')
@click.argument('input_file', nargs=1, type=click.Path(exists=True, readable=True))
@click.argument('output_file', nargs=1, type=click.Path(writable=True))
def _import(input_file, output_file):
    """Read las file and writes as ply file."""
    init(autoreset=True)

    try:
        point_cloud = _load(input_file)
        _save(point_cloud, output_file)
    except ToolException as exc:
        print(Back.RED + "Error: " + str(exc))
