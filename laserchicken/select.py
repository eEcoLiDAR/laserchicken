"""Functions that select points from a point cloud and put them in a new point cloud."""

from laserchicken.keys import point
from laserchicken.utils import copy_point_cloud


def select_equal(point_cloud, attribute, value):
    """
    Return the selection of the input point cloud that contains only points with a given attribute equal to some value.

    :param point_cloud: Input point cloud.
    :param attribute: The attribute name used for selection
    :param value: The value to compare the attribute to
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, point_cloud)
    mask = point_cloud[point][attribute]['data'] == value
    return copy_point_cloud(point_cloud, mask)


def select_above(point_cloud, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute above some value.

    :param point_cloud: Input point cloud
    :param attribute: The attribute name used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, point_cloud)
    mask = point_cloud[point][attribute]['data'] > threshold
    return copy_point_cloud(point_cloud, mask)


def select_below(point_cloud, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute below some value.

    :param point_cloud: Input point cloud
    :param attribute: The attribute name used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, point_cloud)
    mask = point_cloud[point][attribute]['data'] < threshold
    return copy_point_cloud(point_cloud, mask)


def _check_valid_arguments(attribute, point_cloud):
    """
    Raise if arguments are not valid for select_above/select_below functions.

    :param attribute:
    :param point_cloud:
    :return: None
    """
    if point_cloud is None:
        raise ValueError('Input point cloud cannot be None.')
    if attribute not in point_cloud[point]:
        raise ValueError('Attribute key {} for selection not found in point cloud.'.format(attribute))
