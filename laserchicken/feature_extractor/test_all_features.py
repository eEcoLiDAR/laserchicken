import json
import os

import numpy as np
import pytest

from laserchicken import compute_features, compute_neighborhoods, keys, load
from laserchicken.keys import point
#from laserchicken.feature_extractor import *
from laserchicken.feature_extractor.pulse_penetration_feature_extractor import GROUND_TAGS
from laserchicken.utils import copy_point_cloud
from laserchicken.volume_specification import InfiniteCylinder
from .feature_map import create_default_feature_map, _create_name_extractor_pairs

np.random.seed(1234)

_TEST_FILE_NAME = 'AHN3.ply'
_TEST_NEIGHBORHOODS_FILE_NAME = 'AHN3_1000_random_neighbors.json'
_TEST_DATA_SOURCE = 'testdata'

_CYLINDER = InfiniteCylinder(4)
_PC_260807 = load(os.path.join(_TEST_DATA_SOURCE, _TEST_FILE_NAME))
_PC_1000 = copy_point_cloud(_PC_260807, array_mask=(
    np.random.choice(range(len(_PC_260807[point]['x']['data'])), size=1000, replace=False)))
_PC_10 = copy_point_cloud(_PC_260807, array_mask=(
    np.random.choice(range(len(_PC_260807[point]['x']['data'])), size=10, replace=False)))
_1000_NEIGHBORHOODS_IN_260807 = list(compute_neighborhoods(_PC_260807, _PC_1000, _CYLINDER, sample_size=500))
_10_NEIGHBORHOODS_IN_260807 = list(compute_neighborhoods(_PC_260807, _PC_10, _CYLINDER, sample_size=500))
_260807_NEIGHBORHOODS_IN_10 = list(compute_neighborhoods(_PC_10, _PC_260807, _CYLINDER, sample_size=500))

features_by_name = create_default_feature_map()
feature_names = [name for name in features_by_name]


def test_no_duplicate_feature_registrations():
    pairs = _create_name_extractor_pairs()
    for name, _ in pairs:
        matches = [extractor for extractor_name, extractor in pairs if extractor_name is name]
        np.testing.assert_equal(len(matches), 1,
                                'Duplicate registrations for key "{}" by extractors: {}'.format(name, matches))


@pytest.mark.parametrize("feature", feature_names)
def test_completeTile_consistentOutput(feature):
    target_point_cloud = copy_point_cloud(_PC_1000)
    compute_features(copy_point_cloud(_PC_260807), _1000_NEIGHBORHOODS_IN_260807, target_point_cloud, [feature],
                     volume=_CYLINDER)
    _assert_consistent_attribute_length(target_point_cloud)


@pytest.mark.parametrize("feature", feature_names)
def test_manyTargets_consistentOutput(feature):
    target_point_cloud = copy_point_cloud(_PC_260807)
    compute_features(copy_point_cloud(_PC_10), _260807_NEIGHBORHOODS_IN_10, target_point_cloud, [feature],
                     volume=_CYLINDER)
    _assert_consistent_attribute_length(target_point_cloud)


@pytest.mark.parametrize("feature", feature_names)
def test_xAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(x=0, n=n)
    compute_features(pc, [[] for _ in range(n)], pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_yAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(y=0, n=n)
    compute_features(pc, [[] for _ in range(n)], pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zAllZeros_consistentOutput(feature):
    n = 10
    pc = _create_point_cloud(z=0, n=n)
    compute_features(pc, [[] for _ in range(n)], pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zeroPoints_consistentOutput(feature):
    n = 0
    pc = _create_point_cloud(n=n)
    compute_features(pc, [[] for _ in range(n)], pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_zeroNeighbors_consistentOutput(feature):
    _assert_consistent_output_with_n_neighbors(feature, 0)


@pytest.mark.parametrize("feature", feature_names)
def test_oneNeighbor_consistentOutput(feature):
    _assert_consistent_output_with_n_neighbors(feature, 1)


@pytest.mark.parametrize("feature", feature_names)
def test_twoNeighbors_consistentOutput(feature):
    _assert_consistent_output_with_n_neighbors(feature, 2)


def _assert_consistent_output_with_n_neighbors(feature, n_neighbors):
    n_points = 10
    pc = _create_point_cloud(n=n_points)
    compute_features(pc, [range(n_neighbors) for _ in range(n_points)], pc, [feature], volume=_CYLINDER)
    _assert_consistent_attribute_length(pc)


@pytest.mark.parametrize("feature", feature_names)
def test_inputNotChanged(feature):
    original_environment = _PC_260807
    environment = copy_point_cloud(original_environment)
    original_targets = _PC_10
    targets = copy_point_cloud(original_targets)
    original_neighborhoods = _10_NEIGHBORHOODS_IN_260807
    neighborhoods = [[e for e in l] for l in original_neighborhoods]

    compute_features(environment, neighborhoods, targets, [feature], volume=_CYLINDER)

    _assert_attributes_not_changed(original_environment, environment)
    _assert_attributes_not_changed(original_targets, targets)
    assert json.dumps(original_neighborhoods) == json.dumps(neighborhoods)


def _create_point_cloud(x=None, y=None, z=None, norm_z=None, intensity=None, n=10):
    tag = GROUND_TAGS[0]
    pc = {point: {'x': _create_attribute(n, fill_value=x),
                  'y': _create_attribute(n,fill_value=y),
                  'z': _create_attribute(n,fill_value=z),
                  keys.normalized_height: _create_attribute(n,fill_value=norm_z),
                  keys.intensity: _create_attribute(n,fill_value=intensity),
                  'raw_classification': {'data': np.array([i if i % 2 == 0 else tag for i in range(n)]),
                                         'type': 'float'}}}
    return pc


def _create_attribute(n_points, fill_value=None):
    attribute_data = np.array([fill_value if fill_value is not None else i for i in range(n_points)])
    return {'data': attribute_data, 'type': 'float'}


def _assert_attributes_not_changed(original_point_cloud, new_point_cloud):
    for attribute in original_point_cloud[point]:
        np.testing.assert_array_almost_equal(new_point_cloud[point][attribute]['data'],
                                             original_point_cloud[point][attribute]['data'])


def _assert_consistent_attribute_length(target_point_cloud):
    n_elements = len(target_point_cloud[point]['x']['data'])
    for key in target_point_cloud[point]:
        assert n_elements == len(target_point_cloud[point][key]['data'])
