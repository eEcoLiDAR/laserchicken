import json
import os
from unittest import TestCase

import numpy as np
import pytest

from laserchicken import compute_neighbors
from laserchicken import keys
from laserchicken import read_las
from laserchicken.utils import copy_pointcloud
from laserchicken.volume_specification import InfiniteCylinder
from . import _feature_map
from . import compute_features

np.random.seed(1234)

_test_file_name = 'AHN3.las'
_test_neighborhoods_file_name = 'AHN3_1000_random_neighbors.json'
_test_data_source = 'testdata'

_cylinder = InfiniteCylinder(4)
_pc_260807 = read_las.read(os.path.join(_test_data_source, _test_file_name))
_pc_1000 = copy_pointcloud(_pc_260807, array_mask=(
    np.random.choice(range(len(_pc_260807[keys.point]['x']['data'])), size=1000, replace=False)))
_pc_10 = copy_pointcloud(_pc_260807, array_mask=(
    np.random.choice(range(len(_pc_260807[keys.point]['x']['data'])), size=10, replace=False)))
_1000_neighborhoods_in_260807 = next(compute_neighbors.compute_neighborhoods(_pc_260807, _pc_1000, _cylinder))
_10_neighborhoods_in_260807 = next(compute_neighbors.compute_neighborhoods(_pc_260807, _pc_10, _cylinder))


@pytest.mark.parametrize("feature", [name for name in _feature_map()])
@pytest.mark.skip('during development only')
def test_completeTile_noErrors(feature):
    compute_features(copy_pointcloud(_pc_260807), _1000_neighborhoods_in_260807, 0, copy_pointcloud(_pc_1000),
                     [feature],
                     volume=_cylinder)


@pytest.mark.parametrize("feature", [name for name in _feature_map()])
def test_inputNotChanged(feature):
    original_environment = _pc_260807
    environment = copy_pointcloud(original_environment)
    original_targets = _pc_10
    targets = copy_pointcloud(original_targets)
    original_neighborhoods = _10_neighborhoods_in_260807
    neighborhoods = [[e for e in l] for l in original_neighborhoods]

    compute_features(environment, neighborhoods, 0, targets, [feature],
                     volume=_cylinder)

    assert_attributes_not_changed(original_environment, environment)
    assert_attributes_not_changed(original_targets, targets)
    assert json.dumps(original_neighborhoods) == json.dumps(neighborhoods)


def assert_attributes_not_changed(original_point_cloud, new_point_cloud):
    for attribute in original_point_cloud[keys.point]:
        np.testing.assert_array_almost_equal(new_point_cloud[keys.point][attribute]['data'],
                                             original_point_cloud[keys.point][attribute]['data'])
