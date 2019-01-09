"""Test that the map from feature names to extractor classes is correct."""
import pytest

from laserchicken import feature_extractor

from . import __name__ as test_module_name
from . import Test1FeatureExtractor, Test2FeatureExtractor, Test3FeatureExtractor, TestBrokenFeatureExtractor, TestVectorizedFeatureExtractor


@pytest.fixture(scope='module', autouse=True)
def override_features():
    """Overwrite the available feature extractors with test feature extractors."""
    feature_extractor.FEATURES = feature_extractor._feature_map(test_module_name)
    yield
    feature_extractor.FEATURES = feature_extractor._feature_map(feature_extractor.__name__)


def test__feature_map():
    feature_map = {
        'test1_a': Test1FeatureExtractor,
        'test1_b': Test1FeatureExtractor,
        'test2_a': Test2FeatureExtractor,
        'test2_b': Test2FeatureExtractor,
        'test2_c': Test2FeatureExtractor,
        'test3_a': Test3FeatureExtractor,
        'test_broken': TestBrokenFeatureExtractor,
        'vectorized1': TestVectorizedFeatureExtractor,
        'vectorized2': TestVectorizedFeatureExtractor,
    }
    assert feature_map == feature_extractor._feature_map(test_module_name)
