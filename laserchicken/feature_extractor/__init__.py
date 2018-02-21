"""Feature extractor module."""
import importlib
import re

import numpy as np

from laserchicken import keys, utils
from .eigenvals_feature_extractor import EigenValueFeatureExtractor
from .entropy_feature_extractor import EntropyFeatureExtractor
from .sigma_z_feature_extractor import SigmaZFeatureExtractor
from .height_statistics_feature_extractor import HeightStatisticsFeatureExtractor


def _feature_map(module_name=__name__):
    """Construct a mapping from feature names to feature extractor classes."""
    module = importlib.import_module(module_name)
    return {
        feature_name: extractor
        for name, extractor in vars(module).items() if re.match('^[A-Z][a-zA-Z0-9_]*FeatureExtractor$', name)
        for feature_name in extractor.provides()
        }


FEATURES = _feature_map()


def compute_features(env_point_cloud, neighborhoods, target_point_cloud, feature_names, volume, overwrite=False,
                     **kwargs):
    """
    Compute features for each target and store result as attributes in target point cloud

    :param env_point_cloud: environment point cloud
    :param neighborhoods: list of neighborhoods which are themselves lists of indices referring to the environment
    :param target_point_cloud: point cloud of targets
    :param feature_names: list of features that are to be calculated
    :param volume: object describing the volume that contains the neighborhood points
    :param overwrite: if true, even features that are already in the targets point cloud will be calculated and stored
    :param kwargs: keyword arguments for the individual feature extractors
    :return: None, results are stored in attributes of the target point cloud
    """
    _verify_feature_names(feature_names)
    ordered_features = _make_feature_list(feature_names)

    for feature in ordered_features:
        if (not overwrite) and (feature in target_point_cloud[keys.point]):
            continue  # Skip feature calc if it is already there and we do not overwrite
        extractor = FEATURES[feature]()
        _add_or_update_feature(env_point_cloud, neighborhoods, target_point_cloud, extractor, volume, overwrite, kwargs)
        utils.add_metadata(target_point_cloud, type(extractor).__module__, extractor.get_params())


def _verify_feature_names(feature_names):
    unknown_features = [f for f in feature_names if f not in FEATURES]
    if any(unknown_features):
        raise ValueError('Unknown features selected: {}. Available feature are: {}'
                         .format(', '.join(unknown_features), ', '.join(FEATURES.keys())))


def _add_or_update_feature(env_point_cloud, neighborhoods, target_point_cloud, extractor, volume, overwrite, kwargs):
    n_targets = len(target_point_cloud[keys.point]["x"]["data"])
    for k in kwargs:
        setattr(extractor, k, kwargs[k])
    provided_features = extractor.provides()
    n_features = len(provided_features)
    feature_values = [np.empty(n_targets, dtype=np.float64) for i in range(n_features)]
    for target_index in range(n_targets):
        point_values = extractor.extract(env_point_cloud, neighborhoods[target_index], target_point_cloud,
                                         target_index, volume)
        if n_features > 1:
            for i in range(n_features):
                feature_values[i][target_index] = point_values[i]
        else:
            feature_values[0][target_index] = point_values
    for i in range(n_features):
        feature = provided_features[i]
        if overwrite or (feature not in target_point_cloud[keys.point]):
            target_point_cloud[keys.point][feature] = {"type": np.float64, "data": feature_values[i]}


def _make_feature_list(feature_names):
    feature_list = reversed(_make_feature_list_helper(feature_names))
    seen = set()
    return [f for f in feature_list if not (f in seen or seen.add(f))]


def _make_feature_list_helper(feature_names):
    feature_list = feature_names
    for feature_name in feature_names:
        extractor = FEATURES[feature_name]()
        dependencies = extractor.requires()
        feature_list.extend(dependencies)
        feature_list.extend(_make_feature_list_helper(dependencies))
    return feature_list
