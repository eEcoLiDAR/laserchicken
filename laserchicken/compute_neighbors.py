import sys
import math
import numpy as np
from scipy.spatial import cKDTree
from psutil import virtual_memory

from laserchicken import utils, kd_tree
from laserchicken.volume_specification import Sphere, InfiniteCylinder, Cell, Cube
from laserchicken.keys import point


def frange(x_value, y_value, jump):
    while x_value < y_value:
        yield x_value
        x_value += jump


MEMORY_THRESHOLD = 0.5
POINT_CLOUD_DIST = 10


def compute_cylinder_neighborhood(environment_pc, target_pc, radius):
    """Find the indices of points within a cylindrical neighbourhood (using KD Tree) for a given point of a target
    point cloud among the points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
             the returned indices also contains the index of the target point.
    """
    avg_points_cyl = (radius * radius * math.pi) * POINT_CLOUD_DIST
    x = target_pc[point]['x']['data']

    if len(environment_pc[point]['x']['data']) == 0:
        for _ in x:
            yield [[] for _ in x]
        return

    cyl_size = avg_points_cyl * np.size(x) * sys.getsizeof(int)
    mem_size = virtual_memory().total

    print("Cylinder size in Bytes: %s" % cyl_size)
    print("Memory size in Bytes: %s" % mem_size)

    if cyl_size > mem_size * MEMORY_THRESHOLD:
        y = target_pc[point]['y']['data']

        num_points = int(math.floor(mem_size * MEMORY_THRESHOLD / (avg_points_cyl * sys.getsizeof(int))))
        print("Number of points: %d" % num_points)

        env_tree = kd_tree.get_kdtree_for_pc(environment_pc)

        for i in range(0, np.size(x), num_points):
            box_points = np.column_stack(
                (x[i:min(i + num_points, np.size(x))], y[i:min(i + num_points, np.size(x))]))
            target_box_tree = cKDTree(
                box_points, compact_nodes=False, balanced_tree=False)
            yield target_box_tree.query_ball_tree(env_tree, radius)

    else:
        print("Start tree creation")
        env_tree = kd_tree.get_kdtree_for_pc(environment_pc)
        print("Done with env tree creation")
        target_tree = kd_tree.get_kdtree_for_pc(target_pc)
        print("Done with target tree creation")
        yield target_tree.query_ball_tree(env_tree, radius)


def compute_sphere_neighborhood(environment_pc, target_pc, radius):
    """
    Find the indices of points within a spherical neighbourhood for a given point of a target point cloud among the
    points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
    """
    neighborhoods = compute_cylinder_neighborhood(
        environment_pc, target_pc, radius)

    counter = 0  # Target and neighborhood indices are going to be out of sync in loop below.
    for neighborhood_indices in neighborhoods:
        result = []
        for i, _ in enumerate(neighborhood_indices):
            target_x, target_y, target_z = utils.get_point(target_pc, counter)
            counter += 1
            result_indices = []
            for j in neighborhood_indices[i]:
                env_x, env_y, env_z = utils.get_point(environment_pc, j)
                if abs(target_z - env_z) > radius:
                    continue
                if (env_x - target_x) ** 2 + (env_y - target_y) ** 2 + (env_z - target_z) ** 2 <= radius ** 2:
                    result_indices.append(j)
            result.append(result_indices)
        yield result


def compute_cell_neighborhood(environment_pc, target_pc, side_length):
    """
    Find the indices of points within a square neighbourhood for a given point of a target point cloud among the
    points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param side_length: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
    """

    max_radius = 0.5 * math.sqrt((side_length ** 2) + (side_length ** 2))

    neighbors = compute_cylinder_neighborhood(
        environment_pc, target_pc, max_radius)

    counter = 0  # Target and neighborhood indices are going to be out of sync in loop below.
    for neighborhood_indices in neighbors:
        result = []
        for i, _ in enumerate(neighborhood_indices):
            target_x, target_y, _ = utils.get_point(target_pc, counter)
            counter += 1
            neighbor_indices = neighborhood_indices[i]
            result_indices = []
            for j in neighbor_indices:
                env_x, env_y, _ = utils.get_point(environment_pc, j)
                if ((abs(target_x - env_x)) > 0.5 * side_length) or ((abs(target_y - env_y)) > 0.5 * side_length):
                    continue
                else:
                    result_indices.append(j)
            result.append(result_indices)
        yield result


def compute_cube_neighborhood(environment_pc, target_pc, side_length):
    """
    Find the indices of points within a square neighbourhood for a given point of a target point cloud among the
    points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param side_length: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
    """

    neighbors = compute_cell_neighborhood(
        environment_pc, target_pc, side_length)

    counter = 0
    for neighborhood_indices in neighbors:
        result = []
        for i, _ in enumerate(neighborhood_indices):
            _, _, target_z = utils.get_point(target_pc, counter)
            counter += 1
            neighbor_indices = neighborhood_indices[i]
            result_indices = []
            for j in neighbor_indices:
                _, _, env_z = utils.get_point(environment_pc, j)
                if abs(target_z - env_z) > side_length:
                    continue
                else:
                    result_indices.append(j)
            result.append(result_indices)
        yield result


def compute_neighborhoods(env_pc, target_pc, volume_description, sample_size=None):
    """
    Find a subset of points in a neighbourhood in the environment point cloud for each point in a target point cloud.

    :param env_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param volume_description: volume object that describes the shape and size of the search volume
    :param sample_size: maximum number of neighbors returned per target point; if None (default), all are returned
    :return: indices of neighboring points from the environment point cloud for each target point
    """
    volume_type = volume_description.get_type()

    if volume_type == Cell.TYPE:
        neighbors = compute_cell_neighborhood(env_pc, target_pc, volume_description.side_length)
    elif volume_type == Cube.TYPE:
        neighbors = compute_cube_neighborhood(env_pc, target_pc, volume_description.side_length)
    elif volume_type == Sphere.TYPE:
        neighbors = compute_sphere_neighborhood(env_pc, target_pc, volume_description.radius)
    elif volume_type == InfiniteCylinder.TYPE:
        neighbors = compute_cylinder_neighborhood(env_pc, target_pc, volume_description.radius)
    else:
        raise ValueError(
            'Neighborhood computation error because volume type "{}" is unknown.'.format(volume_type))

    for x in neighbors:
        yield _subsample_if_necessary(x, sample_size)


def _subsample_if_necessary(x, sample_size):
    if sample_size:
        sampled = [_subsample(elements, sample_size) if len(elements) > sample_size else elements for elements in x]
        return sampled
    else:
        return x


def _subsample(neighborhood, sample_size=None):
    return list(np.random.choice(neighborhood, sample_size, replace=False))
