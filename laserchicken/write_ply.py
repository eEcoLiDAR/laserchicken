import os
from collections import OrderedDict

import numpy as np

from laserchicken import keys


def write(point_cloud, path):
    """
    Write the point cloud to a ply-file. Path cannot exist yet.
    :param point_cloud:
    :param path:
    :return:
    """
    if os.path.exists(path):
        # Raise most specific subclass of FileExistsError (3.6) and IOError (2.7).
        raise Exception('Cannot write because path {} already exists.'.format(path))
    with open(path, 'w') as ply:
        _write_header(point_cloud, ply)
        _write_data(point_cloud, ply)


def _write_header(point_cloud, ply):
    ply.write("ply" + '\n')
    ply.write("format ascii 1.0" + '\n')
    _write_comment(point_cloud, ply)
    for elem_name in _get_ordered_elements(point_cloud.keys()):
        get_num_elements = (lambda d: len(d["x"].get("data", []))) if elem_name == keys.point else None
        _write_header_elements(point_cloud, ply, elem_name, get_num_elements=get_num_elements)
    ply.write("end_header" + '\n')


def _write_data(pc, ply):
    delimiter = ' '
    for elem_name in _get_ordered_elements(pc.keys()):
        props = _get_ordered_properties(elem_name, pc[elem_name].keys())
        num_elements = len(pc[elem_name]["x"].get("data", [])) if elem_name == keys.point else 1
        for i in range(num_elements):
            for prop in props:
                data_values = pc[elem_name][prop]["data"]
                if isinstance(data_values, np.ndarray):
                    if prop == props[-1]:
                        ply.write(_format_ply(data_values[i]))
                    else:
                        ply.write(_format_ply(data_values[i]) + delimiter)
                else:
                    if i != 0:
                        raise Exception("Scalar quantity does not have element at index %d" % i)
                    ply.write(_format_ply(data_values))
            ply.write('\n')


def _format_ply(obj):
    return str(obj)


def _get_ordered_elements(elem_names):
    if keys.point in elem_names:
        return [keys.point] + sorted([e for e in elem_names if e not in [keys.point, keys.provenance]])
    else:
        return sorted([e for e in elem_names if e not in [keys.point, keys.provenance]])


def _get_ordered_properties(elem_name, prop_list):
    if elem_name == keys.point:
        return ['x', 'y', 'z'] + [k for k in sorted(prop_list) if k not in ['x', 'y', 'z']]
    else:
        return sorted(prop_list)


def _write_comment(pc, ply):
    log = pc.get(keys.provenance, [])
    if not any(log):
        return

    head = 'comment [\n'
    tail = 'comment ]\n'
    formatted_entries = ',\n'.join(['comment ' + _stringify(entry) for entry in log]) + '\n'
    ply.write(head + formatted_entries + tail)


def _stringify(entry):
    copy = {}
    for key, value in _sort_by_key(entry):
        if key == 'time':
            copy[key] = str(value)
        else:
            copy[key] = value
    return str(copy)


def _sort_by_key(entry):
    key_value_pairs = list(entry.items())
    key_value_pairs.sort(key=lambda key_value_pair: key_value_pair[0])
    return key_value_pairs


def _write_header_elements(pc, ply, element_name, get_num_elements=None):
    if element_name in pc:
        num_elements = get_num_elements(pc[element_name]) if get_num_elements else 1
        ply.write("element %s %d\n" % (element_name, num_elements))
        key_list = _get_ordered_properties(element_name, pc[element_name].keys())
        for key in key_list:
            property_type = pc[element_name][key]["type"]
            property_tuple = ("property", property_type, key)
            ply.write(" ".join(property_tuple) + '\n')
