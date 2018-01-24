import os
import ast
import numpy as np
from dateutil import parser

def read(path, verbose=False):
    if not os.path.exists(path):
        raise IOError('File not found: {}'.format(path))

    with open(path, 'r') as ply:
        try:
            first_line = ply.readline()
        except UnicodeDecodeError:
            first_line = ''

        if 'ply' not in first_line:
            raise ValueError('Not a valid ply file: {}'.format(path))

        index = read_header(ply)
        result = {block['type']: read_block(block, ply) for block in index}
        if verbose:
            print('Header:')
            print('-'*10)
            for i, header_field in enumerate(index):
                print(header_field)
                print(index[i])
                print
            print('\nData:')
            print('-'*10)
            for data_field in result:
                print(data_field)
                print(result['%s' % data_field])

            print('***************************')
            print(result)

        return result


def read_header(ply):
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

    if len(comments) > 0:
        for i, comment_line in enumerate(comments):
            comments[i] = ast.literal_eval(comment_line)
            if comments[i]['time']:
                comments[i]['time'] = parser.parse(comments[i]['time'])

        index.append({'type': 'log', 'log': comments})

    return index


def read_block(block, ply_body):
    if block['type'] == 'log':
        return block['log']
    else:
        properties, property_names = get_properties(block)
        block_type = block['type']
        number_of_elements = block['number_of_elements']

        read_elements(ply_body, properties, property_names, block_type, number_of_elements)

        return properties


def cast(value, value_type):
    if value_type == 'float':
        dtype = np.float32
    elif value_type == 'double':
        dtype = np.float64
    elif value_type == 'int':
        dtype = np.int32
    else:
        raise ValueError('Invalid type: {}'.format(value_type))
    return dtype(value)


def read_elements(ply_body, properties, property_names, block_type, number_of_elements):
    for i in range(number_of_elements):
        line = ply_body.readline()
        values = line.split(' ')
        if len(values) != len(property_names):
            raise ValueError('Error reading line {} of {} list.'.format(i, block_type))
        for p, property_name in enumerate(property_names):
            property_type = properties[property_name]['type']
            value = cast(values[p], property_type)
            properties[property_name]['data'][i] = value


def get_properties(block):
    properties = {}
    property_names = []
    for prop in block['properties']:
        if prop['type'] == 'float':
            dtype = np.float32
        elif prop['type'] == 'double':
            dtype = np.float64
        elif prop['type'] == 'int':
            dtype = np.int32
        else:
            raise ValueError('Property has no valid type: {}'.format(prop))
        property_name = prop['name']
        properties[property_name] = {'type': prop['type'], 'data': np.zeros(block['number_of_elements'], dtype)}
        property_names.append(property_name)
    return properties, property_names
