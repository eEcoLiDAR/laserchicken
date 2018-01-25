"""Test feature extraction."""
import pytest
import numpy as np
from laserchicken import feature_extractor,keys,test_tools

from . import __name__ as test_module_name

# Overwrite the available feature extractors with test feature extractors
feature_extractor.FEATURES = feature_extractor._feature_map(test_module_name)


def _compute_features(target,feature_names,overwrite = False):
    neighborhoods = [[] for i in range(len(target["vertex"]["x"]["data"]))]
    feature_extractor.compute_features({}, neighborhoods, target, feature_names, overwrite)
    return target


def test_extract_single_feature():
    target = test_tools.ComplexTestData.get_point_cloud()
    _compute_features(target,['test3_a'])
    assert ('test1_b' in target[keys.point])
    assert all(target[keys.point]['test3_a']['data'] == target[keys.point]['z']['data'])

def test_extract_multiple_features():
    target = test_tools.ComplexTestData.get_point_cloud()
    feature_names = ['test3_a','test2_b']
    target = _compute_features(target,feature_names)
    assert ('test3_a' in target[keys.point] and 'test2_b' in target[keys.point])

def test_extract_does_not_overwrite():
    target = test_tools.ComplexTestData.get_point_cloud()
    target[keys.point]['test2_b'] = {"type":np.float64,"data":[0.9,0.99,0.999,0.9999]}
    feature_names = ['test3_a','test2_b']
    target = _compute_features(target,feature_names)
    assert (target[keys.point]['test2_b']['data'][2] == 0.999)

def test_extract_can_overwrite():
    target = test_tools.ComplexTestData.get_point_cloud()
    target[keys.point]['test2_b'] = {"type":np.float64,"data":[0.9,0.99,0.999,0.9999]}
    feature_names = ['test3_a','test2_b']
    target = _compute_features(target,feature_names,overwrite = True)
    assert (target[keys.point]['test2_b']['data'][2] == 11.5)
