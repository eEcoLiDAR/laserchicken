import numpy as np


_PLY_IMPLICIT_TO_SHORT_TYPES = {
    "uchar": "u1",
    "char": "i1",
    "ushort": "u2",
    "short": "i2",
    "uint": "u4",
    "int": "i4",
    "float": "f4",
    "double": "f8",
}

_SHORT_TO_SINGLE_CHAR_TYPES = {
    "u1": "B",
    "i1": "b",
    "u2": "H",
    "i2": "h",
    "u4": "I",
    "i4": "i",
    "u8": "q",
    "i8": "Q",
    "f4": "f",
    "f8": "d",
}


def select_valid_attributes(attributes_all, attributes_to_select):
    if attributes_to_select is None:
        raise ValueError('Invalid list of attributes provided.')
    else:
        if ((isinstance(attributes_to_select, str) and attributes_to_select == 'all')
                or 'all' in attributes_to_select):
            return attributes_all
        else:
            invalid_attributes = [el for el in attributes_to_select if el not in attributes_all]
            if not invalid_attributes:
                return ['x', 'y', 'z'] \
                       + [el for el in attributes_to_select if el in attributes_all and el not in 'xyz']
            else:
                raise ValueError('Invalid attributes provided: {}'.format(', '.join(invalid_attributes)))


def convert_to_short_type(type, use_ply_implicit=False):
    """
    Convert python type to short format

    Example:
    >>>> convert_to_short_type('float64')
    "f8"
    >>>> convert_to_short_type('float')
    "f8"
    >>>> convert_to_short_type('float', use_ply_implicit=True)
    "f4"

    :param type: python type string
    :param use_ply_implicit: if true, use implicit PLY types (e.g. float -> f4)
    :return: short type string
    """
    type_to_convert = type
    if (use_ply_implicit and
            type_to_convert in _PLY_IMPLICIT_TO_SHORT_TYPES.keys()):
        type_to_convert = _PLY_IMPLICIT_TO_SHORT_TYPES[type_to_convert]
    dtype = np.dtype(type_to_convert)
    return "".join([el for el in dtype.str
                    if el not in ["<", ">", "|"]])


def convert_to_single_character_type(type, use_ply_implicit=False):
    """
    Convert python type to single character type

    Example:
    >>>> convert_to_single_character_type('float64')
    "d"
    >>>> convert_to_single_character_type('f8')
    "d"
    >>>> convert_to_single_character_type('float')
    "d"
    >>>> convert_to_single_character_type('float', use_ply_implicit=True)
    "f"

    :param type: python type string
    :param use_ply_implicit: if true, use implicit PLY types (e.g. float -> f4)
    :return one character string
    """
    # convert string to np data type and remove byte order character
    type_short = convert_to_short_type(type, use_ply_implicit)
    if type_short not in _SHORT_TO_SINGLE_CHAR_TYPES.keys():
        raise ValueError("Type {} not known! Choose between: {}".format(type,
                                                                        ",".join(_SHORT_TO_SINGLE_CHAR_TYPES.keys())))
    return _SHORT_TO_SINGLE_CHAR_TYPES[type_short]
