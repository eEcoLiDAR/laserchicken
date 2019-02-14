import os
import shutil
import unittest
import pytest

import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal, assert_equal

from laserchicken import keys
from laserchicken.keys import point, normalized_height
from laserchicken.normalization import normalize
from laserchicken.spatial_selections import points_in_polygon_wkt, points_in_polygon_wkt_file, \
    points_in_polygon_shp_file
from laserchicken.test_tools import create_point_cloud
from laserchicken.utils import get_attribute_value


class TestNormalize(unittest.TestCase):
    def test_normalize_empty_point_cloud(self):
        point_cloud = create_point_cloud([], [], [])
        normalized_point_cloud = normalize(point_cloud)
        self.assertTrue(normalized_height in normalized_point_cloud[point])

    def test_normalize_tiny_equal_point_cloud(self):
        point_cloud = create_point_cloud([0, 0, 0], [0, 0, 0], [0, 0, 0])
        normalized_point_cloud = normalize(point_cloud)
        normalized_values = get_attribute_value(normalized_point_cloud, range(3), normalized_height)
        np.testing.assert_allclose(normalized_values, np.array([0, 0, 0]), atol=1e-7)

    def test_normalize_tiny_unequal_point_cloud(self):
        point_cloud = create_point_cloud([0, 0, 0], [0, 0, 0], [1, 2, 3])
        normalized_point_cloud = normalize(point_cloud)
        normalized_values = get_attribute_value(normalized_point_cloud, range(3), normalized_height)
        np.testing.assert_allclose(normalized_values, np.array([0, 1, 2]), atol=1e-7)

    def test_normalize_tiny_unequal_point_cloud_multiple_cells(self):
        """Last of the 3 points is not in the neighborhood of the others."""
        point_cloud = create_point_cloud([0, 0, 5], [0, 0, 0], [1, 2, 3])
        normalized_point_cloud = normalize(point_cloud, cell_size=2)
        normalized_values = get_attribute_value(normalized_point_cloud, range(3), normalized_height)
        np.testing.assert_allclose(normalized_values, np.array([0, 1, 0]), atol=1e-7)

    def test_normalize_provenance_data_present(self):
        """Last of the 3 points is not in the neighborhood of the others."""
        point_cloud = create_point_cloud([0, 0, 5], [0, 0, 0], [1, 2, 3])
        point_cloud.pop(keys.provenance, None)  # Remove any provenance data
        normalized_point_cloud = normalize(point_cloud, cell_size=2)
        print(point_cloud)
        self.assertTrue(keys.provenance in normalized_point_cloud)
