"""Functions for loading and saving a pointcloud from/to file."""
from __future__ import print_function

import os

from colorama import Fore

from . import ToolException
from ..read_las import read as read_las
from ..read_ply import read as read_ply
from ..write_ply import write as write_ply


def _load(filename, reader=None):
    print("Reading the input file", end='')

    if reader is None:
        readers = {
            '.ply': read_ply,
            '.las': read_las,
        }
        ext = os.path.splitext(filename)[1]
        if ext not in readers:
            raise ToolException("Unable to guess the file type from the extension {}, "
                                "please specify a loader argument".format(ext))
        reader = readers[ext]

    point_cloud = reader(filename)
    print(Fore.GREEN + "  [DONE]")
    return point_cloud


def _save(point_cloud, filename, saver=None):

    if os.path.exists(filename):
        raise ToolException("Output file already exists! --> {0}".format(filename))

    output_directory = os.path.dirname(filename)

    if output_directory and not os.path.exists(output_directory):
        raise ToolException("Output file path does not exist! --> {0}".format(output_directory))

    print("File will be saved as {0}".format(filename))

    if saver is None:
        savers = {
            '.ply': write_ply,
        }
        ext = os.path.splitext(filename)[1]
        if ext not in savers:
            raise ToolException("Unable to guess the file type from the extension {}, "
                                "please specify a saver argument".format(ext))
        saver = savers[ext]

    print("Saving, please wait...", end='')
    try:
        saver(point_cloud, filename)
    except Exception as exc:
        print(Fore.RED + "  [ERROR]")
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(exc).__name__, exc.args)
        print(message)
        raise ToolException("Conversion has failed! \nCheck '{}' in laserchicken module.".format(saver))

    print(Fore.GREEN + "  [DONE]")
