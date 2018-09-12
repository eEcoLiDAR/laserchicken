from scipy.spatial import cKDTree
import numpy as np
import weakref
from laserchicken import keys

kd_tree_cache = None


def get_kdtree_for_pc(pc):
    """
    Creates a kdtree of the point cloud based on its x and y attributes.
    :param pc: point cloud
    :return: kdtree object
    """
    index = -1
    xref = weakref.ref(pc[keys.point]["x"]["data"])
    yref = weakref.ref(pc[keys.point]["y"]["data"])
    for i in range(len(kd_tree_cache[0])):
        if xref is kd_tree_cache[0][i] and yref is kd_tree_cache[1][i]:
            index = i
    if index < 0:
        # TODO: Check if kd-tree is serialized to file...
        # If not, build it:
        kd_tree_cache[0].append(xref)
        kd_tree_cache[1].append(yref)
        kd_tree_cache[2].append(_build_kdtree(pc))
        index = len(kd_tree_cache[0]) - 1
    return kd_tree_cache[2][index]


def _build_kdtree(pc):
    points = np.column_stack((pc[keys.point]["x"].get("data", []), pc[keys.point]["y"].get("data", [])))
    return cKDTree(points, compact_nodes=False, balanced_tree=False)


def initialize_cache():
    global kd_tree_cache
    kd_tree_cache = ([], [], [])


initialize_cache()
