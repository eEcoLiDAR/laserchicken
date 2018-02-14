import numpy as np
import datetime
from laserchicken import keys,_version

def get_point(pc,index):
    return pc[keys.point]["x"]["data"][index],pc[keys.point]["y"]["data"][index],pc[keys.point]["z"]["data"][index]


def get_feature(pc,index,featurename):
    return pc[keys.point][featurename]["data"][index]


def get_features(pc,index,featurenames):
    return (pc[keys.point][f]["data"][index] for f in featurenames)


def copy_pointcloud(pc_in, array_mask = None):
    """
    Makes a deep copy of a point cloud dict using the array mask when copying the points.
    :param pc_in: Input point cloud
    :param array_mask: A mask indicating which points to copy.
    :return: The copy including only the masked points.
    """
    result = {}
    for key, value in pc_in.items():
        if isinstance(value, dict):
            new_value = copy_pointcloud(value, array_mask)
        elif isinstance(value, np.ndarray):
            if array_mask is not None:
                new_value = value[array_mask] if any(value) else np.copy(value)
            else:
                new_value = np.copy(value)
        else:
            new_value = value
        result[key] = new_value
    return result


def add_metadata(pc,module,params):
    """
    Adds module metadata to pointcloud provenance
    """
    msg = {"time" : datetime.datetime.utcnow()}
    msg["module"] = module.__name__ if hasattr(module,"__name__") else str(module)
    if(any(params)): msg["parameters"] = params
    msg["version"] = _version.__version__
    if(keys.provenance not in pc):
        pc[keys.provenance] = []
    pc[keys.provenance].append(msg)


def fit_plane_svd(xpts, ypts, zpts):
    """
    Fit a plane to a series of points given as x,y,z coordinates.

    r=Return the normal vector to the plane
    Use the SVD methods described for example here
    https://www.ltu.se/cms_fs/1.51590!/svd-fitting.pdf

    :param x: x coordinate of the points
    :param y: y coordinate of the points
    :param z: z coordinate of the points
    :return: normal vector of the plane
    """
    # check size consistency
    if xpts.size != ypts.size or xpts.size != zpts.size or ypts.size != zpts.size:
        raise AssertionError("coordinate size don't match")
    npts = xpts.size

    # form the A matrix of the coordinate
    a = np.column_stack((xpts, ypts, zpts))
    a -= np.sum(a, 0) / npts

    # compute the SVD
    u, _, _ = np.linalg.svd(a.T)

    # return the normal vector
    return u[:, 2]


def generate_random_points_inplane(nvect, dparam=0, npts=100, eps=0.0):
    """
    Generate a series of point all belonging to a plane.

    :param nvect: normal vector of the plane
    :param dparam: zero point value of the plane
    :param npts: number of points
    :param eps: std of the gaussian noise added to the z values of the planes
    :return: x,y,z coordinate of the points
    """
    if isinstance(nvect, list):
        nvect = np.array(nvect)
    a, b, c = nvect / np.linalg.norm(nvect)
    x, y = np.random.rand(npts), np.random.rand(npts)
    z = (dparam - a * x - b * y) / c + np.random.normal(loc=0., scale=eps, size=npts)
    return x, y, z
