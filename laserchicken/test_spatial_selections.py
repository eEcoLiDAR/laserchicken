import unittest

import numpy as np
import pytest
from numpy.testing import assert_equal, assert_almost_equal

from laserchicken.keys import point
from laserchicken import read_las

class TestSpatialSelection(unittest.TestCase):
    @staticmethod
    def test_polygons_contains():
        """ Selecting all points within a Polygon. """
        pc_in = get_test_data()
        pc_out = select_below_ridiculous_high_z(pc_in)
        assert_equal(len(pc_out[point]['x']['data']), 3)
        assert_points_equal(pc_in, pc_out)
