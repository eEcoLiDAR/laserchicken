import sys
import copy
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
        if n_neighbors == 0:
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
        if n_neighbors == 0:
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
    return {keys.point: {'x': {'type': 'float64', 'data': np.array(x)},
                         'y': {'type': 'float64', 'data': np.array(y)},
                         'z': {'type': 'float64', 'data': np.array(z)}},
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
            new_value = copy.copy(value)
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


def add_to_point_cloud(point_cloud_1, point_cloud_2, add_log=True):
    """
    Add points from a point cloud to another

    :param point_cloud_1: point cloud where points are added (it can be empty)
    :param point_cloud_2: point cloud from which points are taken
    :param add_log: whether to add a log to the point cloud structure
    :return: updated point cloud
    """
    if keys.point in point_cloud_1:
        # check whether second point cloud is valid
        if keys.point not in point_cloud_2:
            raise TypeError('Invalid point cloud provided!')

        # if first point cloud is empty, fill it with attributes of second point cloud
        if len(point_cloud_1[keys.point]['x']['data']) == 0:
            for key, value in copy_point_cloud(point_cloud_2).items():
                point_cloud_1[key] = value
            return point_cloud_1
    else:
        # down the tree structure, the point clouds need to have the same attributes
        attributes_1 = sorted(point_cloud_1.keys())
        attributes_2 = sorted(point_cloud_2.keys())
        if attributes_1 != attributes_2:
            raise AttributeError('Attributes differ: [{}] <-> [{}]'.format(", ".join(attributes_1),
                                                                           ", ".join(attributes_2)))

    for key, value in point_cloud_2.items():
        # if root attributes are missing (e.g. log), add them
        if key not in point_cloud_1:
            point_cloud_1[key] = copy.copy(value)
            continue

        # check type of data to merge
        if not isinstance(point_cloud_1[key], type(value)):
            raise TypeError('Types of attribute {} differ in the two point clouds: '
                            '{} <-> {}'.format(key, type(point_cloud_1[key]), type(value)))

        if isinstance(value, dict):
            add_to_point_cloud(point_cloud_1[key], value, add_log=False)
        elif isinstance(value, list):
            point_cloud_1[key] += value
        elif isinstance(value, np.ndarray):
            point_cloud_1[key] = np.concatenate((point_cloud_1[key], value))
        else:
            # non extendable elements should be identical
            if point_cloud_1[key] != value:
                raise ValueError('Point clouds differ in attribute {}: '
                                 '{} <-> {}'.format(key, point_cloud_1[key], value))
    if add_log:
        add_metadata(point_cloud_1, sys.modules[__name__], 'point clouds merged')
    return point_cloud_1


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


def update_feature(point_cloud, feature_name, value, array_mask=None, add_log=True):
    """
    Update one feature of the point cloud and assign value.
    The feature 
    If the feature does not exist in the point cloud, add it.

    :param point_cloud: point cloud to update the feature
    :param feature_name: name of the feature
    :param value: value of the feature. Can be a signl value or an array
    :param array_mask: A mask indicating which point to update the feature
    :param add_log: whether to add a log to the point cloud structure
    :return: updated point cloud
    """

    # Get and check input data type
    if isinstance(value, np.ndarray):
        data_type = value.dtype.name
    else:
        if isinstance(value, (str, int, float, bool)):
            data_type = type(value).__name__
        else:
           raise TypeError("value must be numpy ndarray, or one in (str, int, float, bool)") 
    
    # Check mask size and type
    if array_mask is not None:
        if array_mask.size != len(point_cloud[keys.point]['x']['data']):
            raise AssertionError("Mask size: {} doesn't match the size of point cloud column: {}".format(array_mask.size, len(point_cloud[keys.point]['x']['data'])))

    # If value is ndarray, it shall have the same length as x, or true elements in mask
    if isinstance(value, np.ndarray):
        if array_mask is None:
            if value.size != len(point_cloud[keys.point]['x']['data']): 
                raise AssertionError("value size: {} doesn't match the size of point cloud column: {}".format(value.size, len(point_cloud[keys.point]['x']['data'])))
        else:
            if value.size != np.sum(array_mask): 
                raise AssertionError("value size: {} doesn't match the number of elements in mask: {}".format(value.size, np.sum(array_mask)))
    
    # Check if the feature exists if not create the column
    if not feature_name in point_cloud[keys.point]:
        point_cloud[keys.point][feature_name] = {'data':np.zeros(len(point_cloud[keys.point]['x']['data']), dtype=data_type),
                                                 'type':data_type}
    
    # Convert data of the feature if necccesary
    if point_cloud[keys.point][feature_name]['type'] != data_type:
        print('Setting data type of {} as {}'.format(feature_name, data_type))
        point_cloud[keys.point][feature_name]['data'] = point_cloud[keys.point][feature_name]['data'].astype(data_type)
        point_cloud[keys.point][feature_name]['type'] = data_type

    # Update the column 
    if array_mask is None:
        point_cloud[keys.point][feature_name]['data'][:] = value
    else:
        point_cloud[keys.point][feature_name]['data'][array_mask] = value

    if add_log:
        add_metadata(point_cloud, sys.modules[__name__], 'add feature {} to point cloud.'.format(feature_name))

    return point_cloud