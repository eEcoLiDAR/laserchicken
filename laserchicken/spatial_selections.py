import math
import shapefile
import shapely
from shapely.geometry import Point
from shapely.errors import WKTReadingError
from shapely.wkt import loads
from shapely.geometry import box
import numpy as np

from laserchicken.keys import point
from laserchicken import kd_tree
from laserchicken.utils import copy_point_cloud


def read_wkt_file(path):
    with open(path) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    return content


def read_shp_file(path):
    try:
        shape = shapefile.Reader(path)
    except:
        raise ValueError('Incorrect path.')
    # first feature of the shapefile
    feature = shape.shapeRecords()[0]
    first = feature.shape.__geo_interface__
    # or shp_geom = shape(first) with PyShp)
    shp_geom = shapely.geometry.shape(first)
    return shp_geom


def _contains(pc, polygon):
    """
    Return indices of points in point cloud that are contained by a polygon, i.e., all points within the boundaries of
    Polygon excluding the ones overlaping Polygon's boundaries.
    :param pc: point cloud in
    :param polygon: containing polygon
    :return: point indices
    """
    x = pc[point]['x']['data']
    y = pc[point]['y']['data']
    points_in = []

    mbr = polygon.envelope
    point_box = box(np.min(x), np.min(y), np.max(x), np.max(y))

    if point_box.intersects(mbr):
        (x_min, y_min, x_max, y_max) = mbr.bounds

        rad = math.ceil(math.sqrt(math.pow(x_max - x_min, 2) +
                                  math.pow(y_max - y_min, 2)) / 2)
        p = [x_min + ((x_max - x_min) / 2), y_min + ((y_max - y_min) / 2)]
        tree = kd_tree.get_kdtree_for_pc(pc)
        indices = np.sort(tree.query_ball_point(x=p, r=rad))

        point_id = 0
        for i in indices:
            if polygon.contains(Point(x[i], y[i])):
                points_in.append(i)
                point_id += 1

    return points_in


def points_in_polygon_wkt(pc, polygons_wkt):
    if pc is None:
        raise ValueError('Input point cloud cannot be None.')
    if polygons_wkt is None:
        raise ValueError('Polygons wkt cannot be None.')
    try:
        polygon = loads(polygons_wkt)
    except WKTReadingError:
        raise ValueError('Polygon is invalid.')
    if isinstance(polygon, shapely.geometry.polygon.Polygon) and polygon.is_valid:
        points_in = _contains(pc, polygon)
    else:
        raise ValueError('It is not a Polygon.')
    return copy_point_cloud(pc, points_in)


def points_in_polygon_wkt_file(pc, polygons_wkt_path):
    if pc is None:
        raise ValueError('Input point cloud cannot be None.')
    if polygons_wkt_path is None:
        raise ValueError('Polygons wkt file path cannot be None.')
    try:
        polygons_wkts = read_wkt_file(polygons_wkt_path)
        polygon = loads(polygons_wkts[0])
    except WKTReadingError:
        raise ValueError('Polygon is invalid.')
    except:
        raise
    if isinstance(polygon, shapely.geometry.polygon.Polygon) and polygon.is_valid:
        points_in = _contains(pc, polygon)
    else:
        raise ValueError('It is not a Polygon.')
    return copy_point_cloud(pc, points_in)


def points_in_polygon_shp_file(pc, polygons_shp_path):
    if pc is None:
        raise ValueError('Input point cloud cannot be None.')
    if polygons_shp_path is None:
        raise ValueError('Polygons shp file path cannot be None.')
    try:
        polygon = read_shp_file(polygons_shp_path)
    except:
        raise
    if isinstance(polygon, shapely.geometry.polygon.Polygon) and polygon.is_valid:
        points_in = _contains(pc, polygon)
    else:
        raise ValueError('It is not a Polygon.')
    return copy_point_cloud(pc, points_in)
