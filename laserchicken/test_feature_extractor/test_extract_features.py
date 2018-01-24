"""Test feature extraction."""
import pytest

from laserchicken import feature_extractor

from . import __name__ as test_module_name

# Overwrite the available feature extractors with test feature extractors
feature_extractor.FEATURES = feature_extractor._feature_map(test_module_name)


def _extract_features(feature_names):
    point_cloud = None
    target = {}
    feature_extractor.extract_features(point_cloud, target, feature_names)
    return target


def test_extract_single_feature():
    target = _extract_features(['test3_a'])
    assert target['test3_a'] == 5


def test_extract_multiple_features():
    result = {
        'test1_a': 0,
        'test1_b': 1,
        'test2_a': 2,
        'test2_b': 3,
        'test2_c': 4,
    }
    feature_names = ['test2_c']
    target = _extract_features(feature_names)
    assert target == result


def test_no_overwrite_existing_feature():
    result = {
        'x': 10,
        'test1_a': 20,
        'test1_b': 2,
    }
    point_cloud = None
    target = {
        'x': 10,
        'test1_a': 20,
    }
    feature_extractor.extract_features(point_cloud, target, ['test1_b'])
    assert target == result


def test_extract_broken_feature():
    point_cloud = None
    target = {}
    feature_names = ['test_broken']
    msg = "TestBrokenFeatureExtractor failed to add feature test_broken to target {}"
    with pytest.raises(AssertionError) as exc:
        feature_extractor.extract_features(point_cloud, target, feature_names)
    assert str(exc.value) == msg
