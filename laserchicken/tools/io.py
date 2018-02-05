"""Functions for loading and saving a pointcloud from/to file."""
from __future__ import print_function

import os

from colorama import Fore

from . import ToolException
from ..read_las import read as read_las
from ..read_ply import read as read_ply
from ..write_ply import write as write_ply

READERS = {
    '.ply': read_ply,
    '.las': read_las,
}

WRITERS = {
    '.ply': write_ply,
}


def _load(filename, reader=None):
    """Load point cloud from filename using reader."""
    print("Reading the input file", end='')

    if reader is None:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in READERS:
            raise ToolException("Unable to guess the file type from the extension {}, "
                                "please specify a reader argument".format(ext))
        reader = READERS[ext]

    point_cloud = reader(filename)
    print(Fore.GREEN + "  [DONE]")
    return point_cloud


def _check_save_path(filename):
    """Check that filename can be used to save the point cloud."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in WRITERS:
        ToolException("Unknown output file format {}, choose from {}".format(ext, list(WRITERS)))

    if os.path.exists(filename):
        raise ToolException("Output file already exists! --> {}".format(filename))

    output_directory = os.path.dirname(filename)

    if output_directory and not os.path.exists(output_directory):
        raise ToolException("Output file path does not exist! --> {}".format(output_directory))


def _save(point_cloud, filename, writer=None):
    """Save point cloud to filename using writer."""
    _check_save_path(filename)
    print("File will be saved as {}".format(filename))

    if writer is None:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in WRITERS:
            raise ToolException("Unable to guess the file type from the extension {}, "
                                "please specify a saver argument".format(ext))
        writer = WRITERS[ext]

    print("Saving, please wait...", end='')
    try:
        writer(point_cloud, filename)
    except Exception as exc:
        print(Fore.RED + "  [ERROR]")
        print("An exception of type {} occurred. Arguments:\n{!r}".format(type(exc).__name__, exc.args))
        raise ToolException("Conversion has failed! \nCheck '{}' in laserchicken module.".format(writer))

    print(Fore.GREEN + "  [DONE]")
