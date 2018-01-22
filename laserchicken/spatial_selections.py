from shapely.geometry import Point

from shapely.wkt import loads
import numpy as np
from laserchicken.keys import point


def read_wkt_file(path):
    with open(path) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    return content


def contains(points, polygon_wkt):
    polygon = loads(polygon_wkt)
    points_in = np.full(points.size, False, dtype=bool)
    point_id = 0
    for i in range(points.size):
        if polygon.contains(points[i]):
            points_in[point_id] = i
            point_id += 1
    return points_in


def create_points(pc):
    x = pc[point]['x']['data']
    y = pc[point]['y']['data']
    points = np.empty(x.size)
    for i in range(x.size):
        points[i] = Point(x[i], y[i])
    return points


def filter_points(pc, points_in):
    x = pc[point]['x']['data']
    y = pc[point]['y']['data']
    z = pc[point]['z']['data']
    new_x = np.full(points_in.size, 0)
    new_y = np.full(points_in.size, 0)
    new_z = np.full(points_in.size, 0)
    for i in range(points_in.size):
        new_x[i] = x[points_in[i]]
        new_y[i] = y[points_in[i]]
        new_z[i] = z[points_in[i]]
    pc[point]['x']['data'] = new_x
    pc[point]['y']['data'] = new_y
    pc[point]['z']['data'] = new_z
    return pc


def points_in_polygon_wkt(pc, polygons_wkt_path):
    polygons_wkts = read_wkt_file(polygons_wkt_path)
    points = create_points(pc)
    points_in = contains(points, polygons_wkts)
    new_pc = filter_points(pc, points_in)
    return new_pc
