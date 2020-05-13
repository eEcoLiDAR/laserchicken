"""Test feature extraction."""
import unittest

import numpy as np
from pytest import raises

from laserchicken import keys, test_tools
from laserchicken.feature_extractor import feature_map, feature_extraction
from laserchicken.feature_extractor.mean_std_coeff_feature_extractor import MeanStdCoeffFeatureExtractor
from laserchicken.feature_extractor.median_feature_extractor import MedianFeatureExtractor
from laserchicken.test_feature_extractor import Test1FeatureExtractor
from laserchicken.utils import get_attribute_value
from laserchicken.volume_specification import Sphere
from .feature_test23 import Test2FeatureExtractor, Test3FeatureExtractor, TestVectorizedFeatureExtractor
from .feature_test_broken import TestBrokenFeatureExtractor


class TestExtractFeatures(unittest.TestCase):
    @staticmethod
    def test_extract_single_feature_has_correct_values_in_pc():
        target = test_tools.ComplexTestData().get_point_cloud()
        _compute_features(target, ['test1_a'])
        assert all(target[keys.point]['test1_a']['data'] == 0.5 * target[keys.point]['z']['data'])

    @staticmethod
    def test_extract_only_requested_feature_ends_up_in_pc():
        target = test_tools.ComplexTestData().get_point_cloud()
        _compute_features(target, ['test3_a'])
        assert 'test1_b' not in target[keys.point]

    @staticmethod
    def test_extract_multiple_features_ends_up_in_pc():
        target = test_tools.ComplexTestData().get_point_cloud()
        feature_names = ['test3_a', 'test2_b']
        target = _compute_features(target, feature_names)
        assert ('test3_a' in target[keys.point] and 'test2_b' in target[keys.point])

    @staticmethod
    def test_extract_can_overwrite():
        target = test_tools.ComplexTestData().get_point_cloud()
        target[keys.point]['test1_a'] = {"type": np.float64, "data": [0.9, 0.99, 0.999, 0.9999]}
        feature_names = ['test3_a', 'test1_a']
        target = _compute_features(target, feature_names)
        assert all(target[keys.point]['test1_a']['data'] == 0.5 * target[keys.point]['z']['data'])

    @staticmethod
    def test_extract_unknown_feature():
        with raises(ValueError):
            target = test_tools.ComplexTestData().get_point_cloud()
            _compute_features(target, ['some_unknown_feature'])

    @staticmethod
    def test_vectorized_chunks():
        """Should not throw error for non requested but provided features."""
        n = 2000000  # enough to be too big for a single chunk
        feature_names = ['vectorized1']
        _create_targets_and_extract_features(feature_names, n)

    @staticmethod
    def test_chunks_all_correct_value():
        """Should not throw error for non requested but provided features."""
        n = 2000000  # enough to be too big for a single chunk
        feature_names = ['vectorized1', 'vectorized2', 'test1_a']
        target = _create_targets_and_extract_features(feature_names, n)

        _assert_feature_name_all_valued(1, 'vectorized1', n, target)
        _assert_feature_name_all_valued(1, 'vectorized2', n, target)
        _assert_feature_name_all_valued(0.5, 'test1_a', n, target)

    @staticmethod
    def test_with_neighborhood_generator():
        """Should run for all extractors without error meaning that neighborhood generator is only iterated once.
        Using actual feature extractors here because test feature extractors don't use neighborhoods. """
        n = 200
        feature_names = ['vectorized1', 'test1_a', 'median_z', 'mean_z']
        x = np.ones(n)
        y = np.ones(n)
        z = np.ones(n)
        target = test_tools.create_point_cloud(x, y, z)
        neighborhoods = ([] for _ in range(len(target["vertex"]["x"]["data"])))
        feature_extraction.compute_features({}, neighborhoods, target, feature_names, Sphere(5))

    def setUp(self) -> None:
        self.original_function = feature_map._get_default_extractors
        feature_map._get_default_extractors = _get_test_extractors
        feature_extraction.FEATURES = feature_map.create_default_feature_map()

    def tearDown(self) -> None:
        feature_map._get_default_extractors = self.original_function
        feature_extraction.FEATURES = feature_map.create_default_feature_map()


def _create_targets_and_extract_features(feature_names, n):
    x = np.ones(n)
    y = np.ones(n)
    z = np.ones(n)
    target = test_tools.create_point_cloud(x, y, z)
    _compute_features(target, feature_names)
    return target


def _assert_feature_name_all_valued(expected, feature_name, n, target):
    v = get_attribute_value(target, range(n), feature_name)
    np.testing.assert_allclose(v, expected)


def _compute_features(target, feature_names):
    neighborhoods = [[] for _ in range(len(target["vertex"]["x"]["data"]))]
    feature_extraction.compute_features({}, neighborhoods, target, feature_names, Sphere(5))
    return target


def _get_test_extractors():
    return [Test1FeatureExtractor(), Test2FeatureExtractor(),
            Test3FeatureExtractor(), TestVectorizedFeatureExtractor(),
            TestBrokenFeatureExtractor(), MedianFeatureExtractor(), MeanStdCoeffFeatureExtractor()]
