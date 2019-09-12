import datetime

import numpy as np

from laserchicken import keys, _version


def get_point(point_cloud, index):
    """
    Get x, y, z tuple of one or more points in a point cloud.

    :param point_cloud: point cloud containing the point of interest
    :param index: index of the point within the point cloud
    :return: x, y, z as a tuple of floats
    """
    return point_cloud[keys.point]["x"]["data"][index], point_cloud[keys.point]["y"]["data"][index], \
           point_cloud[keys.point]["z"]["data"][index]


def get_xyz_per_neighborhood(sourcepc, neighborhoods):
    """
    Get x, y, z tuple for each point in a neighborhood for each neighborhood.
    :param sourcepc:
    :param neighborhoods:
    :return: 3d tensor as a masked array
    """
    max_length = max(map(lambda x: len(x), neighborhoods))

    xyz_grp = np.zeros((len(neighborhoods), 3, max_length))
    mask = np.zeros((len(neighborhoods), 3, max_length))
    for i, neighborhood in enumerate(neighborhoods):
        n_neighbors = len(neighborhood)
        if n_neighbors is 0:
            continue
        x, y, z = get_point(sourcepc, neighborhood)
        xyz_grp[i, 0, :n_neighbors] = x
        xyz_grp[i, 1, :n_neighbors] = y
        xyz_grp[i, 2, :n_neighbors] = z
        mask[i, :, :n_neighbors] = 1
    return np.ma.MaskedArray(xyz_grp, mask == 0)


def get_attributes_per_neighborhood(point_cloud, neighborhoods, attribute_names):
    """
    Get attribute values for each point in a neighborhood for each neighborhood.
    :param point_cloud:
    :param neighborhoods:
    :param attribute_names: list of attribute names
    :return: 3d tensor as a masked array
    """
    max_length = max(map(lambda x: len(x), neighborhoods))

    xyz_grp = np.zeros((len(neighborhoods), (len(attribute_names)), max_length))
    mask = np.zeros((len(neighborhoods), (len(attribute_names)), max_length))
    for i_neighborhood, neighborhood in enumerate(neighborhoods):
        n_neighbors = len(neighborhood)
        if n_neighbors is 0:
            continue
        for i_attribute, attribute_name in enumerate(attribute_names):
            attribute = get_attribute_value(point_cloud, neighborhood, attribute_name)
            xyz_grp[i_neighborhood, i_attribute, :n_neighbors] = attribute
        mask[i_neighborhood, :, :n_neighbors] = 1
    return np.ma.MaskedArray(xyz_grp, mask == 0)


def get_attribute_value(point_cloud, index, attribute_name):
    """
    Get value of a single attribute of a single point in a point cloud.

    :param point_cloud: point cloud containing the point of interest
    :param index: index of the point within the point cloud
    :param attribute_name: attribute name
    :return: value of the attribute of the point
    """
    return point_cloud[keys.point][attribute_name]["data"][index]


def get_features(point_cloud, attribute_names, index=None):
    """
    Get value of each attribute in a list for a single point in a point cloud.

    :param point_cloud: point cloud containing the point of interest
    :param attribute_names: attribute names
    :param index: index of the point within the point cloud
    :return: list of values of the attributes of the point
    """
    if index is None:
        index = list(range(point_cloud[keys.point]['x']["data"].shape[0]))
    return (point_cloud[keys.point][f]["data"][index] for f in attribute_names)


def create_point_cloud(x, y, z):
    """
    Create a point cloud object given only the x y z values.

    :param x: x attribute values
    :param y: y attribute values
    :param z: z attribute values
    :return: point cloud object
    """
    return {keys.point: {'x': {'type': 'float', 'data': np.array(x)},
                         'y': {'type': 'float', 'data': np.array(y)},
                         'z': {'type': 'float', 'data': np.array(z)}},
            keys.point_cloud: {},
            keys.provenance: []
            }


def copy_point_cloud(source_point_cloud, array_mask=None):
    """
    Makes a deep copy of a point cloud dict using the array mask when copying the points.

    :param source_point_cloud: Input point cloud
    :param array_mask: A mask indicating which points to copy.
    :return: The copy including only the masked points.
    """
    result = {}
    for key, value in source_point_cloud.items():
        if isinstance(value, dict):
            new_value = copy_point_cloud(value, array_mask)
        elif isinstance(value, np.ndarray):
            if array_mask is not None:
                new_value = value[array_mask] if any(value) else np.copy(value)
            else:
                new_value = np.copy(value)
        else:
            new_value = value
        result[key] = new_value
    return result


def add_metadata(point_cloud, module, params):
    """
    Adds module metadata to point cloud provenance

    :param point_cloud:
    :param module:
    :param params:
    :return:
    """
    msg = {"time": datetime.datetime.utcnow(),
           "module": module.__name__ if hasattr(module, "__name__") else str(module)}
    if any(params):
        msg["parameters"] = params
    msg["version"] = _version.__version__
    if keys.provenance not in point_cloud:
        point_cloud[keys.provenance] = []
    point_cloud[keys.provenance].append(msg)


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


def fit_plane(x, y, a):
    """
    Fit a plane and return a function that returns a for every given x and y.

    Solves Ax = b where A is the matrix of (x,y) combinations, x are the plane parameters, and b the values.
    Example:
    >>> points = np.random.rand(100, 3)
    >>> f = fit_plane(points[:, 0], points[:, 1], points[:, 2])
    >>> new_points = np.random.rand(10, 3)
    >>> f(new_points[0], new_points [1])

    :param x: x coordinates
    :param y: y coordinates
    :param a: value (for instance height)
    :return: function that returns a for every given x and y
    """
    matrix = np.column_stack((np.ones(x.size), x, y))
    parameters, _, _, _ = np.linalg.lstsq(matrix, a)
    return lambda x_in, y_in: np.stack((np.ones(len(x)), x_in, y_in)).T.dot(parameters)
