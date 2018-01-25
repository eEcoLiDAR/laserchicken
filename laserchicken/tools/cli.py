"""Command line tool definitions."""
from __future__ import print_function

import os

import click
from colorama import Back, init

from . import ToolException
from .._version import __version__
from ..select import select_above, select_below
from ..spatial_selections import points_in_polygon_shp_file, points_in_polygon_wkt, points_in_polygon_wkt_file
from .io import _load, _save


@click.group(chain=True, invoke_without_command=True)
@click.version_option(version=__version__)
@click.argument('input_file', nargs=1, type=click.Path(exists=True, readable=True))
@click.argument('output_file', nargs=1, type=click.Path(writable=True))
def main(input_file, output_file):
    pass


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
    return lambda point_cloud: point_cloud


@main.command('filter_below')
@click.argument('attribute')
@click.argument('threshold', type=click.FLOAT)
def _filter_below(attribute, threshold):
    return lambda point_cloud: select_below(point_cloud, attribute, threshold)


@main.command('filter_above')
@click.argument('attribute')
@click.argument('threshold', type=click.FLOAT)
def _filter_above(attribute, threshold):
    return lambda point_cloud: select_above(point_cloud, attribute, threshold)


@main.command('points_in_polygon')
@click.argument('polygon')
def _point_in_polygon(polygon):
    if os.path.isfile(polygon):
        ext = os.path.splitext(polygon)[1].lower()
        functions = {
            '.shp': points_in_polygon_shp_file,
            '.wkt': points_in_polygon_wkt_file,
        }
        if ext not in functions:
            raise ToolException("Unable to determine type of shapefile, choose from types {}".format)
        return lambda point_cloud: functions[ext](point_cloud, polygon)
    else:
        print("polygon is not a file, assuming it is a WKT string")
        return lambda point_cloud: points_in_polygon_wkt(point_cloud, polygon)
