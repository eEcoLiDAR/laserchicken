from shapely.geometry import Point

from shapely.wkt import loads
import numpy as np
from laserchicken.keys import point


def read_wkt_file(path):
    with open(path) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    return content


def contains(pc, polygon_wkt):
    polygon = loads(polygon_wkt)
    x = pc[point]['x']['data']
    y = pc[point]['y']['data']

    points_in = []
    point_id = 0
    for i in range(x.size):
        if polygon.contains(Point(x[i], y[i])):
            points_in.append(i)
            point_id += 1
    return points_in

def filter_points(pc, points_in):
    x = pc[point]['x']['data']
    y = pc[point]['y']['data']
    z = pc[point]['z']['data']
    new_x = np.full(len(points_in), 0)
    new_y = np.full(len(points_in), 0)
    new_z = np.full(len(points_in), 0)
    for i in range(len(points_in)):
        new_x[i] = x[points_in[i]]
        new_y[i] = y[points_in[i]]
        new_z[i] = z[points_in[i]]
    pc[point]['x']['data'] = new_x
    pc[point]['y']['data'] = new_y
    pc[point]['z']['data'] = new_z
    return pc


def points_in_polygon_wkt(pc, polygons_wkt_path):
    polygons_wkts = read_wkt_file(polygons_wkt_path)
    points_in = contains(pc, polygons_wkts[0])
    new_pc = filter_points(pc, points_in)
    return new_pc
