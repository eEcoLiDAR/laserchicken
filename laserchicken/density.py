from shapely.geometry import Point, MultiPoint

import numpy as np
from laserchicken.keys import point
import math

def area_density_(pc, r):
    rad = r
    if (rad == None):
        x = pc[point]['x']['data']
        y = pc[point]['y']['data']
        points = []
        for i in range(len(x)):
            points.append(Point(x[i], y[i]))
        multi_point = MultiPoint(points)
        mbr = multi_point.convex_hull.envelope
        (x_min, y_min, x_max, y_max) = mbr.bounds

        rad = math.ceil(math.sqrt(math.pow(x_max - x_min, 2) + math.pow(y_max - y_min, 2)) / 2)

    if (rad <= 0):
        raise ValueError("The radious should bigger than zero.")

    area = math.pi*math.pow(rad,2)

    return len(x)/area

def volume_density_(pc, r):
    rad = r
    if (rad == None):
        x = pc[point]['x']['data']
        y = pc[point]['y']['data']
        points = []
        for i in range(len(x)):
            points.append(Point(x[i], y[i]))
        multi_point = MultiPoint(points)
        mbr = multi_point.convex_hull.envelope
        (x_min, y_min, x_max, y_max) = mbr.bounds

        rad = math.ceil(math.sqrt(math.pow(x_max - x_min, 2) + math.pow(y_max - y_min, 2)) / 2)

    if (rad <= 0):
        raise ValueError("The radious should bigger than zero.")

    z = pc[point]['z']['data']
    volume = math.pi*math.pow(rad,2) * (np.max(z) - np.min(z))

    return len(x)/volume

def area_density(pc):
    return area_density_(pc, None)

def area_density_rad(pc, rad):
    return area_density_(pc, rad)

def volume_density(pc):
    return volume_density_(pc, None)

def volume_density_rad(pc, rad):
    return volume_density_(pc, rad)