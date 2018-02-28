"""Test feature extraction."""
import unittest

import numpy as np
import pytest
from pytest import raises

from laserchicken import feature_extractor, keys, test_tools
from laserchicken.volume_specification import Sphere

from . import __name__ as test_module_name


class TestExtractFeatures(unittest.TestCase):
    @staticmethod
    def test_extract_single_feature():
        target = test_tools.ComplexTestData.get_point_cloud()
        _compute_features(target, ['test3_a'])
        assert 'test1_b' in target[keys.point]
        assert all(target[keys.point]['test3_a']['data'] == target[keys.point]['z']['data'])

    @staticmethod
    def test_extract_multiple_features():
        target = test_tools.ComplexTestData.get_point_cloud()
        feature_names = ['test3_a', 'test2_b']
        target = _compute_features(target, feature_names)
        assert ('test3_a' in target[keys.point] and 'test2_b' in target[keys.point])

    @staticmethod
    def test_extract_does_not_overwrite():
        target = test_tools.ComplexTestData.get_point_cloud()
        target[keys.point]['test2_b'] = {"type": np.float64, "data": [0.9, 0.99, 0.999, 0.9999]}
        feature_names = ['test3_a', 'test2_b']
        target = _compute_features(target, feature_names)
        assert target[keys.point]['test2_b']['data'][2] == 0.999

    @staticmethod
    def test_extract_can_overwrite():
        target = test_tools.ComplexTestData.get_point_cloud()
        target[keys.point]['test2_b'] = {"type": np.float64, "data": [0.9, 0.99, 0.999, 0.9999]}
        feature_names = ['test3_a', 'test2_b']
        target = _compute_features(target, feature_names, overwrite=True)
        assert target[keys.point]['test2_b']['data'][2] == 11.5

    @staticmethod
    def test_extract_unknown_feature():
        with raises(ValueError):
            target = test_tools.ComplexTestData.get_point_cloud()
            _compute_features(target, ['some_unknown_feature'])


@pytest.fixture(scope='module', autouse=True)
def override_features():
    """Overwrite the available feature extractors with test feature extractors."""
    feature_extractor.FEATURES = feature_extractor._feature_map(test_module_name)
    yield
    feature_extractor.FEATURES = feature_extractor._feature_map(feature_extractor.__name__)


def _compute_features(target, feature_names, overwrite=False):
    neighborhoods = [[] for i in range(len(target["vertex"]["x"]["data"]))]
    feature_extractor.compute_features({}, neighborhoods, target, feature_names, Sphere(5), overwrite)
    return target
