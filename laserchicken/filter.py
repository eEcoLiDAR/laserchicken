"""Functions that select points from a point cloud and put them in a new point cloud."""

import math
import os
import shapefile
import shapely
import sys
from shapely.geometry import Point
from shapely.errors import WKTReadingError
from shapely.wkt import loads
from shapely.geometry import box
import numpy as np

from laserchicken.keys import point
from laserchicken import kd_tree
from laserchicken.utils import copy_point_cloud, add_metadata


def select_equal(point_cloud, attribute, value):
    """
    Return the selection of the input point cloud that contains only points with a given attribute equal to some value.

    :param point_cloud: Input point cloud.
    :param attribute: The attribute name used for selection
    :param value: The value to compare the attribute to
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, point_cloud)
    mask = point_cloud[point][attribute]['data'] == value
    point_cloud_filtered = copy_point_cloud(point_cloud, mask)
    add_metadata(point_cloud_filtered, sys.modules[__name__],
                 {'attribute': attribute, 'value': value})
    return point_cloud_filtered


def select_above(point_cloud, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute above some value.

    :param point_cloud: Input point cloud
    :param attribute: The attribute name used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, point_cloud)
    mask = point_cloud[point][attribute]['data'] > threshold
    point_cloud_filtered = copy_point_cloud(point_cloud, mask)
    add_metadata(point_cloud_filtered, sys.modules[__name__],
                 {'attribute': attribute, 'threshold': threshold})
    return point_cloud_filtered


def select_below(point_cloud, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute below some value.

    :param point_cloud: Input point cloud
    :param attribute: The attribute name used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, point_cloud)
    mask = point_cloud[point][attribute]['data'] < threshold
    point_cloud_filtered = copy_point_cloud(point_cloud, mask)
    add_metadata(point_cloud_filtered, sys.modules[__name__],
                 {'attribute': attribute, 'threshold': threshold})
    return point_cloud_filtered


def _check_valid_arguments(attribute, point_cloud):
    """
    Raise if arguments are not valid for select_above/select_below functions.

    :param attribute:
    :param point_cloud:
    :return: None
    """
    if point_cloud is None:
        raise ValueError('Input point cloud cannot be None.')
    if attribute not in point_cloud[point]:
        raise ValueError('Attribute key {} for selection not found in point cloud.'.format(attribute))


def select_polygon(point_cloud, polygon_string, read_from_file=False, return_mask=False):
    """
    Return the selection of the input point cloud that contains only points within a given polygon.

    :param point_cloud: Input point cloud
    :param polygon_string: Polygon, either defined in a WKT string or in a file (WKT and ESRI formats supported)
    :param read_from_file: if true, polygon is expected to be the name of the file where the polygon is defined
    :param return_mask: if true, return a mask of selected points, rather than point cloud
    :return:
    """
    if point_cloud is None:
        raise ValueError('Input point cloud cannot be None.')
    if not isinstance(polygon_string, str):
        raise ValueError('Polygon (or its filename) should be a string')
    if read_from_file:
        format = os.path.splitext(polygon_string)[1].lower()
        reader = _get_polygon_reader(format)
        polygon = reader(polygon_string)
    else:
        polygon = _load_polygon(polygon_string)
    
    if isinstance(polygon, shapely.geometry.polygon.Polygon) and polygon.is_valid:
        points_in = _contains(point_cloud, polygon)
    elif isinstance(polygon,shapely.geometry.multipolygon.MultiPolygon) and polygon.is_valid:
        points_in = []
        count=1
        for poly in polygon:
            if not(count%200) or count==len(polygon):
                print('Checking polygon {}/{}...'.format(count, len(polygon)))
            points_in.extend(_contains(point_cloud, poly))
            count=count+1
        print('{} points found in {} polygons.'.format(len(points_in), len(polygon)))
    else:
        raise ValueError('It is not a Polygon or Multipolygon.')
    
    if return_mask: 
        mask = np.zeros(len(point_cloud['vertex']['x']['data']), dtype=bool)
        mask[points_in] = True
        return mask
    else:
        point_cloud_filtered = copy_point_cloud(point_cloud, points_in)
        add_metadata(point_cloud_filtered, sys.modules[__name__],
                    {'polygon_string': polygon_string,
                    'read_from_file': read_from_file})
        return point_cloud_filtered


def _read_wkt_file(path):
    with open(path) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    return _load_polygon(content[0])


def _read_shp_file(path):
    shape = shapefile.Reader(path)
    # first feature of the shapefile
    feature = shape.shapeRecords()[0]
    first = feature.shape.__geo_interface__
    # or shp_geom = shape(first) with PyShp)
    shp_geom = shapely.geometry.shape(first)
    return shp_geom


polygon_readers = {
    '.wkt': _read_wkt_file,
    '.shp': _read_shp_file
}


def _get_polygon_reader(format):
    if format not in polygon_readers:
        raise NotImplementedError(
            'Polygon file format {} unknown. Implemented formats are:'.format(format, ','.join(polygon_readers.keys())))
    else:
        return polygon_readers[format]


def _load_polygon(string):
    try:
        return loads(string)
    except WKTReadingError:
        raise ValueError('Polygon is invalid. --> {}'.format(string))


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
