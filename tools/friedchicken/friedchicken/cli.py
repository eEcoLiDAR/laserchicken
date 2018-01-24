import os.path

import click

from laserchicken.read_las import read
from laserchicken.write_ply import write


@click.command()
@click.option('--lasfile', '-l', required=True, prompt='enter the las filename',
              help='Name of the input las file.')
@click.option('--plyfile', '-p', default='out.ply', prompt='enter the ply filename',
              help='Name of the output ply file.')

def main(lasfile, plyfile):
    """Reads las file and writes as ply file."""

    if plyfile:
        print("Used ply flag")
    else:
        print("NOT Used ply flag!")

    if plyfile == "out.ply":
        click.echo('No ply file was provided...')

    click.echo('{0}, {1}.'.format(lasfile, plyfile))

    # more checks are needed here
    print("Checking the input file")
    if os.path.isfile(lasfile):
        point_cloud = read(lasfile)
    else:
        print("Either file is missing or is not readable!")

    print("Writing the ply file...")
    write(point_cloud, plyfile)
