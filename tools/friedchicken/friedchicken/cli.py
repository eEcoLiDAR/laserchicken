from __future__ import print_function

import os.path
import sys

import click
from colorama import Fore, Back, Style
from colorama import init


from laserchicken.read_las import read
from laserchicken.write_ply import write

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 0.1.0')
    ctx.exit()


@click.command()
@click.option('--lasfile', '-l', required=True,
              help='Name of the input las file.')
@click.option('--plyfile', '-p', required=True,
              help='Name of the output ply file.')
@click.option('-v', '--verbose', count=True)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)

def main(lasfile, plyfile, verbose):
    """Reads las file and writes as ply file."""
    if (verbose):
        click.echo('Verbosity: %s' % verbose)

    init(autoreset=True)
    # more checks are needed here
    print("Checking the input file", end='')
    if os.path.isfile(lasfile):
        point_cloud = read(lasfile)
    else:
        print(Fore.RED + "  [ERROR]")
        print(Back.RED + "Either file is missing or is not readable!")
        sys.exit(1)
    print(Fore.GREEN + "  [DONE]")

    output_directory = os.path.dirname(plyfile)
    if output_directory == "":
        output_directory = "./"
        plyfile = output_directory + plyfile

    if os.path.exists(plyfile):
        print(Back.RED + "Output file already exists! --> {0}".format(plyfile))
        sys.exit(1)

    if not os.path.exists(output_directory) and output_directory != "":
        print(Back.RED + "Output file path does not exist! --> {0}".format(output_directory))
        sys.exit(1)
    else:
        print("File will be saved as {0}".format(plyfile))

    print("Frying the chicken, please wait...", end='')
    try:
        write(point_cloud, plyfile)
        print(Fore.GREEN + "  [YUMMY]")
    except:
        print(Fore.RED + "  [ERROR]")
        print(Back.RED + "Convertion has failed! \nCheck 'write_ply' file in laserchicken module.")

def print_help_msg(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))
