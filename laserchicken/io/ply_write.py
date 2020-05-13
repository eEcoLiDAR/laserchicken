import json
import numpy as np

from struct import pack

from laserchicken import keys
from laserchicken.io.utils import convert_to_single_character_type, select_valid_attributes


def write(point_cloud, path, attributes='all', is_binary=False):
    """
    Write the point cloud to a ply-file.
    :param point_cloud:
    :param attributes: write only the specified attributes ('all' to write all of them)
    :param path:
    :param is_binary:
    :return:
    """
    if keys.point in point_cloud:
        attributes = select_valid_attributes([attr for attr in point_cloud[keys.point].keys()], attributes)
    with open(path, 'w') as ply:
        _write_header(point_cloud, attributes, ply, is_binary)
    with open(path, ''.join(['a', 'b' if is_binary else ''])) as ply:
        _write_data(point_cloud, attributes, ply, is_binary)


def _write_header(point_cloud, attributes, ply, is_binary=False):
    ply.write("ply" + '\n')
    if is_binary:
        file_type = "binary_little_endian"
    else:
        file_type = "ascii"
    ply.write("format %s 1.0\n" % file_type)
    _write_comment(point_cloud, ply)
    for elem_name in _get_ordered_elements(point_cloud.keys()):
        get_num_elements = (lambda d: len(d["x"].get("data", []))) if elem_name == keys.point else None
        _write_header_elements(point_cloud, attributes, ply, elem_name, get_num_elements=get_num_elements)
    ply.write("end_header" + '\n')


def _write_data(pc, attributes, ply, is_binary=False):
    for elem_name in _get_ordered_elements(pc.keys()):
        if elem_name == keys.point:
            props = attributes
        else:
            props = pc[elem_name].keys()
        props = _get_ordered_properties(elem_name, props)
        num_elements = len(pc[elem_name]["x"].get("data", [])) if elem_name == keys.point else 1
        for i in range(num_elements):
            line_elements = []
            line_types = []
            for prop in props:
                data_values, data_type = _get_data_and_type(pc[elem_name][prop])
                if isinstance(data_values, np.ndarray):
                    line_elements.append(_format_ply(data_values[i], is_binary))
                else:
                    if i != 0:
                        raise Exception("Scalar quantity does not have element at index %d" % i)
                    line_elements.append(_format_ply(data_values, is_binary))
                line_types.append(convert_to_single_character_type(data_type, use_ply_implicit=True))
            if is_binary:
                # add leading byte order character (< for little endian)
                format = ''.join(["<"] + line_types)
                line = pack(format, *line_elements)
            else:
                line = " ".join(line_elements) + "\n"
            ply.write(line)


def _get_data_and_type(attribute):
    return attribute["data"], attribute["type"]


def _format_ply(obj, is_binary):
    if is_binary:
        return obj
    else:
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
    formatted_entries = ',\n'.join(['comment ' + json.dumps(_stringify(entry), sort_keys=True) for entry in log]) + '\n'
    ply.write(head + formatted_entries + tail)


def _stringify(entry):
    copy = {}
    for key, value in _sort_by_key(entry):
        if isinstance(value, dict):
            copy[key] = _stringify(value)
        elif isinstance(value, list):
            copy[key] = [_stringify(entry) if isinstance(entry, dict) else entry for entry in value]
        else:
            if key == 'time':
                copy[key] = str(value)
            else:
                copy[key] = value
    return copy


def _sort_by_key(entry):
    key_value_pairs = list(entry.items())
    key_value_pairs.sort(key=lambda key_value_pair: key_value_pair[0])
    return key_value_pairs


def _write_header_elements(pc, attributes, ply, element_name, get_num_elements=None):
    if element_name in pc:
        num_elements = get_num_elements(pc[element_name]) if get_num_elements else 1
        ply.write("element %s %d\n" % (element_name, num_elements))
        if element_name == keys.point:
            key_list = attributes
        else:
            key_list = pc[element_name].keys()
        key_list = _get_ordered_properties(element_name, key_list)
        for key in key_list:
            property_type = pc[element_name][key]["type"]
            property_tuple = ("property", property_type, key)
            ply.write(" ".join(property_tuple) + '\n')
