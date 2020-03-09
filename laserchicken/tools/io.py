"""Functions for loading and saving a pointcloud from/to file."""
from __future__ import print_function

from colorama import Fore

from . import ToolException
from laserchicken import load, export


def _load(filename):
    """Load point cloud from filename using reader."""
    print("Reading the input file", end='')
    point_cloud = load(filename)
    print(Fore.GREEN + "  [DONE]")
    return point_cloud


def _save(point_cloud, filename, writer=None):
    """Save point cloud to filename using writer."""
    print("File will be saved as {}".format(filename))
    print("Saving, please wait...", end='')
    try:
        export(point_cloud, filename)
    except Exception as exc:
        print(Fore.RED + "  [ERROR]")
        print("An exception of type {} occurred. Arguments:\n{!r}".format(type(exc).__name__, exc.args))
        raise ToolException("Conversion has failed! \nCheck '{}' in laserchicken module.".format(writer))

    print(Fore.GREEN + "  [DONE]")
