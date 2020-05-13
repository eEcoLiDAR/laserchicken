"""Command line tool definitions."""
from __future__ import print_function

import os

import click
from colorama import Back, init

from . import ToolException
from .._version import __version__
from ..filter import select_above, select_below, select_polygon
from .io import _load, _save


@click.group(chain=True, invoke_without_command=True)
@click.version_option(version=__version__)
@click.argument('input_file', nargs=1, type=click.Path(exists=True, readable=True))
@click.argument('output_file', nargs=1, type=click.Path(writable=True))
def main(input_file, output_file):
    """Various commmands for selecting points from a point cloud.

    Note that commands can be chained.

    Example:

    laserchicken testdata/AHN3.las test.ply filter_below intensity 100 filter_above intensity 60
    """


@main.resultcallback()
def process_pipeline(processors, input_file, output_file):
    init(autoreset=True)
    try:
        point_cloud = _load(input_file)
        for processor in processors:
            point_cloud = processor(point_cloud)
        _save(point_cloud, output_file)
    except ToolException as exc:
        print(Back.RED + "Error: " + str(exc))


@main.command('import')
def _import():
    """Read data from input file and save to output file.

    Actually the word import can be omitted, as this is the default operation.

    Examples:

    laserchicken testdata/AHN2.las test.ply

    laserchicken testdata/AHN2.las test.ply import
    """
    return lambda point_cloud: point_cloud


@main.command('filter_below')
@click.argument('attribute')
@click.argument('threshold', type=click.FLOAT)
def _filter_below(attribute, threshold):
    """Select those points where the value of attribute is below threshold.

    Example:

    laserchicken testdata/AHN3.las test.ply filter_below intensity 100
    """
    return lambda point_cloud: select_below(point_cloud, attribute, threshold)


@main.command('filter_above')
@click.argument('attribute')
@click.argument('threshold', type=click.FLOAT)
def _filter_above(attribute, threshold):
    """Select those points where the value of attribute is above threshold.

    Example:

    laserchicken testdata/AHN3.las test.ply filter_above intensity 100
    """
    return lambda point_cloud: select_above(point_cloud, attribute, threshold)


@main.command('filter_in_polygon')
@click.argument('polygon')
def _filter_in_polygon(polygon):
    """Select those points that are inside polygon.

    Polygon can be a shape file (with extension .shp or .wkt) or a WKT string.

    Examples:

    laserchicken testdata/AHN2.las test.ply filter_in_polygon testdata/ahn2_geometries_shp/ahn2_polygon.shp

    laserchicken testdata/AHN2.las test.ply filter_in_polygon testdata/ahn2_geometries_wkt/ahn2_polygon.wkt

    laserchicken testdata/AHN2.las test.ply filter_in_polygon 'POLYGON(( 243590.0 572110.0, 243640.0 572160.0, 243700.0 572110.0, 243640.0 572060.0, 243590.0 572110.0 ))'
    """
    if os.path.isfile(polygon):
        return lambda point_cloud: select_polygon(point_cloud, polygon, read_from_file=True)
    else:
        print("polygon is not a file, assuming it is a WKT string")
        return lambda point_cloud: select_polygon(point_cloud, polygon, read_from_file=False)
