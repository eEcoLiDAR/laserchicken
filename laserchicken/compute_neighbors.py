from laserchicken import utils, kd_tree
from laserchicken.volume_specification import Sphere, InfiniteCylinder
from laserchicken.keys import point
from laserchicken.spatial_selections import _contains

import sys
import numpy as np
from scipy.spatial import cKDTree
from psutil import virtual_memory
import math
from shapely.geometry import box

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

MEMORY_THRESHOLD = 0.5
POINTCLOUD_DIST = 10


def compute_cylinder_neighborhood_(environment_pc, target_pc, radius):
    """Find the indices of points within a cylindrical neighbourhood (using KD Tree)
    for a given point of a target point cloud among the points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
             the returned indices also contains the index of the target point.
    """
    avg_points_cyl = (radius*radius*math.pi)*POINTCLOUD_DIST
    x = target_pc[point]['x']['data']

    cyl_size = avg_points_cyl * np.size(x) * sys.getsizeof(int)
    mem_size = virtual_memory().total

    print("Cylinder size in Bytes: %s" % cyl_size)
    print("Memory size in Bytes: %s" % mem_size)

    if (cyl_size > mem_size*MEMORY_THRESHOLD):
      y = target_pc[point]['y']['data']
      x_min = np.min(x)
      x_max = np.max(x)
      y_min = np.min(y)
      y_max = np.max(y)

      num_fragments = math.ceil(math.sqrt(cyl_size / (mem_size*MEMORY_THRESHOLD)))
      print("Number of fragments: %d" % num_fragments)

      x_step = (x_max - x_min)/num_fragments
      y_step = (y_max - y_min)/num_fragments

      points_in = []
      env_tree = kd_tree.get_kdtree_for_pc(environment_pc)
      target_tree = kd_tree.get_kdtree_for_pc(target_pc)
      for x_curr in frange(x_min, x_max, x_step):
        for y_curr in frange(y_min, y_max, y_step):
          target_box = box(x_curr, y_curr, (x_curr + x_step - 1), (y_curr + y_step - 1))
          target_box_ind = _contains(target_pc,target_box)
          target_box_x = target_pc[point]["x"].get("data", [])
          target_box_y = target_pc[point]["y"].get("data", [])

          box_points = np.column_stack(([target_box_x[i] for i in target_box_ind], [target_box_y[i] for i in target_box_ind]))
          target_box_tree = cKDTree(box_points, compact_nodes=False, balanced_tree=False)
          yield target_box_tree.query_ball_tree(env_tree, radius)
    else:
      print("Start tree creation")
      env_tree = kd_tree.get_kdtree_for_pc(environment_pc)
      print("Done with env tree creation")
      target_tree = kd_tree.get_kdtree_for_pc(target_pc)
      print("Done with target tree creation")
      yield target_tree.query_ball_tree(env_tree, radius)


def compute_cylinder_neighborhood(environment_pc, target_pc, radius):
    """Find the indices of points within a cylindrical neighbourhood (using KD Tree)
    for a given point of a target point cloud among the points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
             the returned indices also contains the index of the target point.
    """

    print("Start tree creation")
    env_tree = kd_tree.get_kdtree_for_pc(environment_pc)
    print("Done with env tree creation")
    target_tree = kd_tree.get_kdtree_for_pc(target_pc)
    print("Done with target tree creation")
    return target_tree.query_ball_tree(env_tree, radius)


def compute_sphere_neighborhood_(environment_pc, target_pc, radius):
    """
    Find the indices of points within a spherical neighbourhood for a given point of a target point cloud among
    the points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
    """

    neighbors = compute_cylinder_neighborhood_(environment_pc, target_pc, radius)

    for neighborhood_indices in neighbors:
      result = []
      for i in range(len(neighborhood_indices)):
        target_x, target_y, target_z = utils.get_point(target_pc, i)
        neighbor_indices = neighborhood_indices[i]
        result_indices = []
        for j in neighbor_indices:
          env_x, env_y, env_z = utils.get_point(environment_pc, j)
          if abs(target_z - env_z) > radius:
            continue
          if (env_x - target_x) ** 2 + (env_y - target_y) ** 2 + (env_z - target_z) ** 2 <=  radius ** 2 :
            result_indices.append(j)
        result.append(result_indices)
      yield result


def compute_sphere_neighborhood(environment_pc, target_pc, radius):
    """
    Find the indices of points within a spherical neighbourhood for a given point of a target point cloud among
    the points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
    """

    neighborhood_indices = compute_cylinder_neighborhood_(environment_pc, target_pc, radius)

    result = []
    for i in range(len(neighborhood_indices)):
      target_x, target_y, target_z = utils.get_point(target_pc, i)
      neighbor_indices = neighborhood_indices[i]
      result_indices = []
      for j in neighbor_indices:
        env_x, env_y, env_z = utils.get_point(environment_pc, j)
        if abs(target_z - env_z) > radius:
          continue
        if (env_x - target_x) ** 2 + (env_y - target_y) ** 2 + (env_z - target_z) ** 2 <=  radius ** 2 :
          result_indices.append(j)
      result.append(result_indices)
    return result


def compute_neighborhoods_(env_pc, target_pc, volume_description):
    """
    Find a subset of points in a neighbourhood in the environment point cloud for each point in a target point cloud.

    :param env_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param volume_description: volume object that describes the shape and size of the search volume
    :return: indices of neighboring points from the environment point cloud for each target point
    """
    volume_type = volume_description.get_type()
    if volume_type == Sphere.TYPE:
      compute_neighborhoods = compute_sphere_neighborhood_(env_pc, target_pc, volume_description.radius)
    elif volume_type == InfiniteCylinder.TYPE:
      compute_neighborhoods = compute_cylinder_neighborhood_(env_pc, target_pc, volume_description.radius)
    else:
      raise ValueError('Neighborhood computation error because volume type "{}" is unknown.'.format(volume_type))
    for x in compute_neighborhoods:
      yield x


def compute_neighborhoods(env_pc, target_pc, volume_description):
    """
    Find a subset of points in a neighbourhood in the environment point cloud for each point in a target point cloud.

    :param env_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param volume_description: volume object that describes the shape and size of the search volume
    :return: indices of neighboring points from the environment point cloud for each target point
    """
    volume_type = volume_description.get_type()
    if volume_type == Sphere.TYPE:
      compute_neighborhoods = compute_sphere_neighborhood(env_pc, target_pc, volume_description.radius)
    elif volume_type == InfiniteCylinder.TYPE:
      compute_neighborhoods = compute_cylinder_neighborhood(env_pc, target_pc, volume_description.radius)
    return compute_neighborhoods
    raise ValueError('Neighborhood computation error because volume type "{}" is unknown.'.format(volume_type))
