import json
import os
from unittest import TestCase

import numpy as np
import pytest

from laserchicken import compute_neighbors
from laserchicken import keys
from laserchicken import read_las
from laserchicken.keys import point
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
_260807_neighborhoods_in_10 = next(compute_neighbors.compute_neighborhoods(_pc_10, _pc_260807, _cylinder))

feature_names = [name for name in _feature_map()]


@pytest.mark.parametrize("feature", feature_names)
def test_completeTile_consistentOutput(feature):
    target_point_cloud = copy_pointcloud(_pc_1000)
    compute_features(copy_pointcloud(_pc_260807), _1000_neighborhoods_in_260807, 0, target_point_cloud,
                     [feature], volume=_cylinder)
    _assert_consistent_attribute_length(target_point_cloud)


@pytest.mark.parametrize("feature", feature_names)
def test_manyTargets_consistentOutput(feature):
    target_point_cloud = copy_pointcloud(_pc_260807)
    compute_features(copy_pointcloud(_pc_10), _260807_neighborhoods_in_10, 0, target_point_cloud,
                     [feature], volume=_cylinder)
    _assert_consistent_attribute_length(target_point_cloud)


@pytest.mark.parametrize("feature", feature_names)
def test_xAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(x=0, n=n)
    compute_features(pc, range(n), 0, pc, [feature], volume=_cylinder)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_yAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(y=0, n=n)
    compute_features(pc, range(n), 0, pc, [feature], volume=_cylinder)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(z=0, n=n)
    compute_features(pc, range(n), 0, pc, [feature], volume=_cylinder)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zeroPoints_consistentOutput(feature):
    n = 0
    pc = _create_point_cloud(n=n)
    compute_features(pc, [[] for _ in range(n)], 0, pc, [feature], volume=_cylinder)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zeroNeighbors_consistentOutput(feature):
    _test_consistent_output_with_n_neighbors(feature, 0)


@pytest.mark.parametrize("feature", feature_names)
def test_oneNeighbor_consistentOutput(feature):
    _test_consistent_output_with_n_neighbors(feature, 1)


@pytest.mark.parametrize("feature", feature_names)
def test_twoNeighbors_consistentOutput(feature):
    _test_consistent_output_with_n_neighbors(feature, 2)


def _test_consistent_output_with_n_neighbors(feature, n_neighbors):
    n_points = 10
    pc = _create_point_cloud(n=n_points)
    compute_features(pc, [range(n_neighbors) for _ in range(n_points)], 0, pc, [feature], volume=_cylinder)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_oneNeighbor_consistentOutput(feature):
    n = 1
    pc = _create_point_cloud(n=n)
    compute_features(pc, [[] for _ in range(n)], 0, pc, [feature], volume=_cylinder)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_inputNotChanged(feature):
    original_environment = _pc_260807
    environment = copy_pointcloud(original_environment)
    original_targets = _pc_10
    targets = copy_pointcloud(original_targets)
    original_neighborhoods = _10_neighborhoods_in_260807
    neighborhoods = [[e for e in l] for l in original_neighborhoods]

    compute_features(environment, neighborhoods, 0, targets, [feature],
                     volume=_cylinder)

    _assert_attributes_not_changed(original_environment, environment)
    _assert_attributes_not_changed(original_targets, targets)
    assert json.dumps(original_neighborhoods) == json.dumps(neighborhoods)


def _create_point_cloud(x=None, y=None, z=None, n=10):
    pc = {point: {'x': {'data': np.array([x if x is not None else i for i in range(n)]), 'type': 'float'},
                  'y': {'data': np.array([y if y is not None else i for i in range(n)]), 'type': 'float'},
                  'z': {'data': np.array([z if z is not None else i for i in range(n)]), 'type': 'float'}}}
    return pc


def _assert_attributes_not_changed(original_point_cloud, new_point_cloud):
    for attribute in original_point_cloud[keys.point]:
        np.testing.assert_array_almost_equal(new_point_cloud[keys.point][attribute]['data'],
                                             original_point_cloud[keys.point][attribute]['data'])


def _assert_consistent_attribute_length(target_point_cloud):
    n_elements = len(target_point_cloud[keys.point]['x'])
    for key in target_point_cloud[keys.point]:
        print(key, len(target_point_cloud[keys.point][key]))
        assert n_elements == len(target_point_cloud[keys.point][key])
