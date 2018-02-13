import numpy as np
import datetime
from laserchicken import keys, _version


def get_point(point_cloud, index):
    """
    Get x, y, z tuple of a single point in a point cloud.

    :param point_cloud: point cloud containing the point of interest
    :param index: index of the point within the point cloud
    :return: x, y, z as a tuple of floats
    """
    return point_cloud[keys.point]["x"]["data"][index], point_cloud[keys.point]["y"]["data"][index], point_cloud[keys.point]["z"]["data"][index]


def get_attribute_value(point_cloud, index, attribute_name):
    """
    Get value of a single attribute of a single point in a point cloud.

    :param point_cloud: point cloud containing the point of interest
    :param index: index of the point within the point cloud
    :param attribute_name: attribute name
    :return: value of the attribute of the point
    """
    return point_cloud[keys.point][attribute_name]["data"][index]


def get_features(point_cloud, index, attribute_names):
    """
    Get value of each attribute in a list for a single point in a point cloud.

    :param point_cloud: point cloud containing the point of interest
    :param index: index of the point within the point cloud
    :param attribute_names: attribute names
    :return: list of values of the attributes of the point
    """
    return (point_cloud[keys.point][f]["data"][index] for f in attribute_names)


def copy_pointcloud(source_point_cloud, array_mask=None):
    """
    Makes a deep copy of a point cloud dict using the array mask when copying the points.

    :param source_point_cloud: Input point cloud
    :param array_mask: A mask indicating which points to copy.
    :return: The copy including only the masked points.
    """
    result = {}
    for key, value in source_point_cloud.items():
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
