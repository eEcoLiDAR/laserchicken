"""Test that the map from feature names to extractor classes is correct."""
from laserchicken.feature_extractor import _feature_map
from . import __name__ as module_name, Test1FeatureExtractor, Test2FeatureExtractor, Test3FeatureExtractor


def test__feature_map():
    feature_map = {
        'test1_a': Test1FeatureExtractor,
        'test1_b': Test1FeatureExtractor,
        'test2_a': Test2FeatureExtractor,
        'test2_b': Test2FeatureExtractor,
        'test2_c': Test2FeatureExtractor,
        'test3_a': Test3FeatureExtractor,
    }
    assert feature_map == _feature_map(module_name)
