"""Command line tool definitions."""
from __future__ import print_function

import os

import click
from colorama import Back, init

from . import ToolException
from .._version import __version__
from ..select import select_above, select_below
from ..spatial_selections import points_in_polygon_shp_file, points_in_polygon_wkt, points_in_polygon_wkt_file
from .io import check_save_path, load, save


@click.group(chain=True)
@click.version_option(version=__version__)
def main():
    """Operate on point clouds using various commands.

    Example:

    laserchicken import testdata/AHN2.las test.ply
    laserchicken filter_below testdata/AHN3.las test.ply intensity 100
    laserchicken filter_below testdata/AHN3.las test.ply intensity 60
    laserchicken filter_above --help
    """
    init(autoreset=True)


@main.command('import')
@click.argument('input_file', nargs=1, type=click.Path(exists=True, readable=True))
@click.argument('output_file', nargs=1, type=click.Path(writable=True))
def _import(input_file, output_file):
    """Read data from input file and save to output file.

    Examples:

    laserchicken import testdata/AHN2.las test.ply
    """
    _process(lambda point_cloud: point_cloud, input_file, output_file)


def _process(func, input_file, output_file):
    try:
        check_save_path(output_file)
        point_cloud_in = load(input_file)
        point_cloud_out = func(point_cloud_in)
        save(point_cloud_out, output_file)
    except ToolException as exc:
        print(Back.RED + "Error: " + str(exc))


@main.command('filter_below')
@click.argument('input_file', nargs=1, type=click.Path(exists=True, readable=True))
@click.argument('output_file', nargs=1, type=click.Path(writable=True))
@click.argument('attribute')
@click.argument('threshold', type=click.FLOAT)
def _filter_below(input_file, output_file, attribute, threshold):
    """Select those points where the value of attribute is below threshold.

    Example:

    laserchicken filter_below testdata/AHN3.las test.ply intensity 100
    """
    _process(lambda point_cloud: select_below(point_cloud, attribute, threshold), input_file, output_file)


@main.command('filter_above')
@click.argument('input_file', nargs=1, type=click.Path(exists=True, readable=True))
@click.argument('output_file', nargs=1, type=click.Path(writable=True))
@click.argument('attribute')
@click.argument('threshold', type=click.FLOAT)
def _filter_above(input_file, output_file, attribute, threshold):
    """Select those points where the value of attribute is above threshold.

    Example:

    laserchicken testdata/AHN3.las test.ply filter_above intensity 100
    """
    _process(lambda point_cloud: select_above(point_cloud, attribute, threshold), input_file, output_file)


@main.command('filter_in_polygon')
@click.argument('input_file', nargs=1, type=click.Path(exists=True, readable=True))
@click.argument('output_file', nargs=1, type=click.Path(writable=True))
@click.argument('polygon')
def _filter_in_polygon(input_file, output_file, polygon):
    """Select those points that are inside polygon.

    Polygon can be a shape file (with extension .shp or .wkt) or a WKT string.

    Examples:

    laserchicken testdata/AHN2.las test.ply filter_in_polygon testdata/ahn2_geometries_shp/ahn2_polygon.shp

    laserchicken testdata/AHN2.las test.ply filter_in_polygon testdata/ahn2_geometries_wkt/ahn2_polygon.wkt

    laserchicken testdata/AHN2.las test.ply filter_in_polygon 'POLYGON(( 243590.0 572110.0, 243640.0 572160.0, 243700.0 572110.0, 243640.0 572060.0, 243590.0 572110.0 ))'
    """
    if os.path.isfile(polygon):
        ext = os.path.splitext(polygon)[1].lower()
        functions = {
            '.shp': points_in_polygon_shp_file,
            '.wkt': points_in_polygon_wkt_file,
        }
        if ext not in functions:
            raise ToolException("Unable to determine type of shapefile, "
                                "choose from types {}".format(list(functions)))
        _process(lambda point_cloud: functions[ext](point_cloud, polygon), input_file, output_file)
    else:
        print("polygon is not a file, assuming it is a WKT string")
        _process(lambda point_cloud: points_in_polygon_wkt(point_cloud, polygon), input_file, output_file)
