import os
import ast
import numpy as np
from dateutil import parser


def read(path):
    """
    Read point cloud data from a ply file.
    :param path: path to the ply file
    :return: dictionary containing the point cloud data
    """
    if not os.path.exists(path):
        raise IOError('File not found: {}'.format(path))

    with open(path, 'r') as ply:
        try:
            first_line = ply.readline()
        except UnicodeDecodeError:
            first_line = ''

        if 'ply' not in first_line:
            raise ValueError('Not a valid ply file: {}'.format(path))

        index = _read_header(ply)
        return {block['type']: _read_block(block, ply) for block in index}


def _read_header(ply):
    index = []
    comments = []
    line = ply.readline()
    while line.strip() != 'end_header':
        if line.startswith('element'):
            element_type = line.split()[1]
            number_of_elements = int(line.split()[2])
            current_properties = []
            index.append(
                {'type': element_type, 'number_of_elements': number_of_elements, 'properties': current_properties})

        if line.startswith('property'):
            property_type, property_name = line[9:].strip('\n').split(' ')
            current_properties.append({'type': property_type, 'name': property_name})

        if line.startswith('comment'):
            comment_line = line.strip('\n').split(' ', 1)[1]
            comments.append(comment_line)

        line = ply.readline()

    index.append({'type': 'log', 'log': (_read_log(comments))})
    return index


def _read_log(comments):
    try:
        log = ast.literal_eval(''.join(comments)) if comments else []
    except(SyntaxError):  # Log can't be read. Maybe a ply file with 'regular' comments and no log.
        log = []
    for i, entry in enumerate(log):
        if 'time' in entry:
            entry['time'] = parser.parse(entry['time'])
    return log


def _read_block(block, ply_body):
    if block['type'] == 'log':
        return block['log']
    else:
        properties, property_names = _get_properties(block)
        block_type = block['type']
        number_of_elements = block['number_of_elements']

        _read_elements(ply_body, properties, property_names, block_type, number_of_elements)

        return properties


def _cast(value, value_type):
    dtype = np.dtype(value_type)
    return dtype.type(value)


def _read_elements(ply_body, properties, property_names, block_type, number_of_elements):
    for i in range(number_of_elements):
        line = ply_body.readline()
        values = line.split(' ')
        if len(values) != len(property_names):
            raise ValueError('Error reading line {} of {} list.'.format(i, block_type))
        for p, property_name in enumerate(property_names):
            property_type = properties[property_name]['type']
            value = _cast(values[p], property_type)
            properties[property_name]['data'][i] = value


def _get_properties(block):
    properties = {}
    property_names = []
    for prop in block['properties']:
        dtype = np.dtype(prop['type'])
        property_name = prop['name']
        properties[property_name] = {'type': prop['type'], 'data': np.zeros(block['number_of_elements'], dtype)}
        property_names.append(property_name)
    return properties, property_names
