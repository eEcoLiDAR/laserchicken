import ast
import numpy as np
from dateutil import parser
from struct import unpack, calcsize

from laserchicken.io.utils import convert_to_short_type, convert_to_single_character_type


def read(path):
    """
    Read point cloud data from a ply file.
    :param path: path to the ply file
    :return: dictionary containing the point cloud data
    """
    # check whether file is in ascii/binary format
    is_binary = _is_ply_binary(path)

    # read file content
    with open(path, ''.join(['r', 'b' if is_binary else ''])) as ply:
        first_line = _read_header_line(ply, is_binary)

        if 'ply' not in first_line:
            raise ValueError('Not a valid ply file: {}'.format(path))

        index, format = _read_header(ply, is_binary)
        return {block['type']: _read_block(block, ply, format) for block in index}


def _is_ply_binary(path, is_binary=False):
    is_valid = True
    with open(path, ''.join(['r', 'b' if is_binary else ''])) as ply:
        try:
            _ = _read_header_line(ply, is_binary)
        except UnicodeDecodeError:
            if is_binary:
                is_valid = False
            else:
                return _is_ply_binary(path, is_binary=True)
    if not is_valid:
        raise ValueError('Not a valid ply file: {}'.format(path))
    return is_binary


def _read_header(ply, is_binary=False):
    index = []
    comments = []
    line = _read_header_line(ply, is_binary)
    format = line.split()[1]
    while line.strip() != 'end_header':
        if line.startswith('element'):
            element_type = line.split()[1]
            number_of_elements = int(line.split()[2])
            current_properties = []
            index.append(
                {'type': element_type, 'number_of_elements': number_of_elements, 'properties': current_properties})

        if line.startswith('property'):
            property_type, property_name = line[9:].rstrip().split(' ')
            current_properties.append({'type': property_type, 'name': property_name})

        if line.startswith('comment'):
            comment_line = line.rstrip().split(' ', 1)[1]
            comments.append(comment_line)

        line = _read_header_line(ply, is_binary)

    index.append({'type': 'log', 'log': (_read_log(comments))})
    return index, format


def _read_header_line(ply, is_binary=False):
    line = ply.readline()
    if not is_binary:
        return line
    else:
        return line.decode('utf-8')


def _read_log(comments):
    try:
        log = ast.literal_eval(' '.join(comments)) if comments else []
    except SyntaxError:  # Log can't be read. Maybe a ply file with 'regular' comments and no log.
        log = []
    for i, entry in enumerate(log):
        if 'time' in entry:
            entry['time'] = parser.parse(entry['time'])
    return log


def _read_block(block, ply_body, format='ascii'):
    if block['type'] == 'log':
        return block['log']
    else:
        properties, property_names = _get_properties(block)
        block_type = block['type']
        number_of_elements = block['number_of_elements']

        if format == 'ascii':
            _read_elements_ascii(ply_body, properties, property_names, block_type, number_of_elements)
        else:
            _read_elements_binary(ply_body, properties, property_names, block_type, number_of_elements, format)

        return properties


def _cast(value, value_type):
    dtype = np.dtype(value_type)
    return dtype.type(value)


def _read_elements_ascii(ply_body, properties, property_names, block_type, number_of_elements):
    for i in range(number_of_elements):
        line = ply_body.readline()
        values = line.split()
        if len(values) != len(property_names):
            raise ValueError('Error reading line {} of {} list.'.format(i, block_type))
        for p, property_name in enumerate(property_names):
            property_type = properties[property_name]['type']
            value = _cast(values[p], property_type)
            properties[property_name]['data'][i] = value


def _read_elements_binary(ply_body, properties, property_names, block_type, number_of_elements, bin_format):
    if bin_format == 'binary_little_endian':
        byte_ordering = '<'
    elif bin_format == 'binary_big_endian':
        byte_ordering = '>'
    else:
        raise ValueError('Unable to read: unknown binary format {}.'.format(bin_format))

    format_list = [convert_to_single_character_type(properties[name]['type'])
                   for name in property_names]
    format = ''.join([byte_ordering] + format_list)
    buffer_size = calcsize(format)
    for i in range(number_of_elements):
        buffer = ply_body.read(buffer_size)
        try:
            values = unpack(format, buffer)
        except Exception as err:
            raise ValueError('{}; error at line {} of {} list.'.format(str(err), i, block_type))
        for p, property_name in enumerate(property_names):
            properties[property_name]['data'][i] = values[p]


def _get_properties(block):
    properties = {}
    property_names = []
    for prop in block['properties']:
        dtype = np.dtype(convert_to_short_type(prop['type'], use_ply_implicit=True))
        property_name = prop['name']
        properties[property_name] = {'type': dtype.name, 'data': np.zeros(block['number_of_elements'], dtype)}
        property_names.append(property_name)
    return properties, property_names
