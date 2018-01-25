import numpy as np
from laserchicken.utils import copy_pointcloud
from laserchicken.keys import point



def select_above(pc, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute above some value.
    :param pc: Input point cloud
    :param attribute: The attribute name used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, pc)
    mask = pc[point][attribute]['data'] > threshold
    return copy_pointcloud(pc, mask)


def select_below(pc, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute below some value.
    :param pc: Input point cloud
    :param attribute: The attribute name used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, pc)
    mask = pc[point][attribute]['data'] < threshold
    return copy_pointcloud(pc, mask)


def _check_valid_arguments(attribute, pc):
    """
    Raises if arguments are not valid for select_above/select_below functions.
    :param attribute:
    :param pc:
    :return:
    """
    if pc is None:
        raise ValueError('Input point cloud cannot be None.')
    if attribute not in pc[point]:
        raise ValueError('Attribute key {} for selection not found in point cloud.'.format(attribute))
