import json
import os

import pytest
import numpy as np
from laserchicken import compute_neighbors
from laserchicken import keys
from laserchicken import read_las
from laserchicken.feature_extractor.pulse_penetration_feature_extractor import GROUND_TAGS
from laserchicken.keys import point
from laserchicken.utils import copy_point_cloud
from laserchicken.volume_specification import InfiniteCylinder

from . import _feature_map
from . import compute_features

np.random.seed(1234)

_TEST_FILE_NAME = 'AHN3.las'
_TEST_NEIGHBORHOODS_FILE_NAME = 'AHN3_1000_random_neighbors.json'
_TEST_DATA_SOURCE = 'testdata'

_CYLINDER = InfiniteCylinder(4)
_PC_260807 = read_las.read(os.path.join(_TEST_DATA_SOURCE, _TEST_FILE_NAME))
_PC_1000 = copy_point_cloud(_PC_260807, array_mask=(
    np.random.choice(range(len(_PC_260807[keys.point]['x']['data'])), size=1000, replace=False)))
_PC_10 = copy_point_cloud(_PC_260807, array_mask=(
    np.random.choice(range(len(_PC_260807[keys.point]['x']['data'])), size=10, replace=False)))
_1000_NEIGHBORHOODS_IN_260807 = next(
    compute_neighbors.compute_neighborhoods(_PC_260807, _PC_1000, _CYLINDER, sample_size=500))
_10_NEIGHBORHOODS_IN_260807 = next(
    compute_neighbors.compute_neighborhoods(_PC_260807, _PC_10, _CYLINDER, sample_size=500))
_260807_NEIGHBORHOODS_IN_10 = next(
    compute_neighbors.compute_neighborhoods(_PC_10, _PC_260807, _CYLINDER, sample_size=500))

feature_names = [name for name in _feature_map()]


@pytest.mark.parametrize("feature", feature_names)
def test_completeTile_consistentOutput(feature):
    target_point_cloud = copy_point_cloud(_PC_1000)
    compute_features(copy_point_cloud(_PC_260807), _1000_NEIGHBORHOODS_IN_260807, 0, target_point_cloud,
                     [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(target_point_cloud)


@pytest.mark.parametrize("feature", feature_names)
def test_manyTargets_consistentOutput(feature):
    target_point_cloud = copy_point_cloud(_PC_260807)
    compute_features(copy_point_cloud(_PC_10), _260807_NEIGHBORHOODS_IN_10, 0, target_point_cloud,
                     [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(target_point_cloud)

@pytest.mark.parametrize("feature", feature_names)
def test_manyTargetsBigEnvironment_consistentOutput(feature):
    target_point_cloud = copy_point_cloud(_PC_260807)
    compute_features(copy_point_cloud(_PC_1000), _260807_NEIGHBORHOODS_IN_10, 0, target_point_cloud,
                     [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(target_point_cloud)


@pytest.mark.parametrize("feature", feature_names)
def test_xAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(x=0, n=n)
    compute_features(pc, [[] for _ in range(n)], 0, pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_yAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(y=0, n=n)
    compute_features(pc, [[] for _ in range(n)], 0, pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(z=0, n=n)
    compute_features(pc, [[] for _ in range(n)], 0, pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zeroPoints_consistentOutput(feature):
    n = 0
    pc = _create_point_cloud(n=n)
    compute_features(pc, [[] for _ in range(n)], 0, pc, [feature], volume=_CYLINDER)
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
    compute_features(pc, [range(n_neighbors) for _ in range(n_points)], 0, pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_inputNotChanged(feature):
    original_environment = _PC_260807
    environment = copy_point_cloud(original_environment)
    original_targets = _PC_10
    targets = copy_point_cloud(original_targets)
    original_neighborhoods = _10_NEIGHBORHOODS_IN_260807
    neighborhoods = [[e for e in l] for l in original_neighborhoods]

    compute_features(environment, neighborhoods, 0, targets, [feature],
                     volume=_CYLINDER)

    _assert_attributes_not_changed(original_environment, environment)
    _assert_attributes_not_changed(original_targets, targets)
    assert json.dumps(original_neighborhoods) == json.dumps(neighborhoods)


def _create_point_cloud(x=None, y=None, z=None, n=10):
    tag = GROUND_TAGS[0]
    pc = {point: {'x': {'data': np.array([x if x is not None else i for i in range(n)]), 'type': 'float'},
                  'y': {'data': np.array([y if y is not None else i for i in range(n)]), 'type': 'float'},
                  'z': {'data': np.array([z if z is not None else i for i in range(n)]), 'type': 'float'},
                  'raw_classification': {'data': np.array([i if i % 2 == 0 else tag for i in range(n)]),
                                         'type': 'float'}}}
    return pc


def _assert_attributes_not_changed(original_point_cloud, new_point_cloud):
    for attribute in original_point_cloud[keys.point]:
        np.testing.assert_array_almost_equal(new_point_cloud[keys.point][attribute]['data'],
                                             original_point_cloud[keys.point][attribute]['data'])


def _assert_consistent_attribute_length(target_point_cloud):
    n_elements = len(target_point_cloud[keys.point]['x'])
    for key in target_point_cloud[keys.point]:
        assert n_elements == len(target_point_cloud[keys.point][key])
