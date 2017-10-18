import os
from plyfile import PlyData


def write(pc, path):
    PlyData().write(path)
