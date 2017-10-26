import numpy as np


def select_above(pc, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute above some value.
    :param pc: Input point cloud
    :param attribute: The attribute used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, pc)
    mask = pc['points'][attribute]['data'] > threshold
    return _copy_dict(pc, mask)


def select_below(pc, attribute, threshold):
    """
    Return the selection of the input point cloud that contains only points with a given attribute below some value.
    :param pc: Input point cloud
    :param attribute: The attribute used for selection
    :param threshold: The threshold value used for selection
    :return: A new point cloud containing only the selected points
    """
    _check_valid_arguments(attribute, pc)
    mask = pc['points'][attribute]['data'] < threshold
    return _copy_dict(pc, mask)


def _check_valid_arguments(attribute, pc):
    """
    Raises if arguments are not valid for select_above/select_below functions.
    :param attribute:
    :param pc:
    :return:
    """
    if pc is None:
        raise ValueError('Input point cloud cannot be None.')
    if attribute not in pc['points']:
        raise ValueError('Attribute key {} for selection not found in point cloud.'.format(attribute))


def _copy_dict(pc_in, array_mask):
    """
    Makes a deep copy of a point cloud dict using the array mask when copying the points.
    :param pc_in: Input point cloud
    :param array_mask: A mask indicating which points to copy.
    :return: The copy including only the masked points.
    """
    result = {}
    for key, value in pc_in.items():
        if isinstance(value, dict):
            new_value = _copy_dict(value, array_mask)
        elif isinstance(value, np.ndarray):
            new_value = value[array_mask]
        else:
            new_value = value
        result[key] = new_value
    return result
