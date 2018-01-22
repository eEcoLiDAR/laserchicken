from shapely.geometry import Point

from shapely.wkt import loads
import numpy as np
from laserchicken.keys import point
import shapefile
import shapely

def read_wkt_file(path):
    with open(path) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    return content


def contains(pc, polygon):
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

def read_shp_file(path):
    shape = shapefile.Reader(path)
    # first feature of the shapefile
    feature = shape.shapeRecords()[0]
    first = feature.shape.__geo_interface__
    shp_geom = shapely.geometry.shape(first)  # or shp_geom = shape(first) with PyShp)
    return shp_geom

def points_in_polygon_wkt(pc, polygons_wkt_path):
    polygons_wkts = read_wkt_file(polygons_wkt_path)
    polygon = loads(polygons_wkts[0])
    points_in = contains(pc, polygon)
    new_pc = filter_points(pc, points_in)
    return new_pc

def points_in_polygon_shp(pc, polygons_shp_path):
    polygon = read_shp_file(polygons_shp_path)
    points_in = contains(pc, polygon)
    new_pc = filter_points(pc, points_in)
    return new_pc
