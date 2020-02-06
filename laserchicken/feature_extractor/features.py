"""Feature extractor module."""

import numpy as np
import sys

import time

from laserchicken import keys, utils
from laserchicken.feature_extractor import FEATURES

def compute_features(env_point_cloud, neighborhoods, target_idx_base, target_point_cloud, feature_names, volume,
                     overwrite=False, verbose=True, **kwargs):
    """
    Compute features for each target and store result as point attributes in target point cloud.

    Example:
    >>> point_cloud = load('data1.ply')
    >>> target_point_cloud = load('data2.ply')
    >>> volume = volume_specification.InfiniteCylinder(4)
    >>> neighbors = compute_neighborhoods(point_cloud, target_point_cloud, volume)
    >>> neighborhoods = []
    >>> for x in neighbors:
    >>>   neighborhoods += x
    >>> compute_features(point_cloud, neighborhoods, target_point_cloud, ['eigenv_1', 'kurto_z'], volume)
    >>> eigenv_1 = target_point_cloud[point]['eigenv_1']['data']

    Results of the example above are stored in the target point cloud as extra point attributes.

    :param env_point_cloud: environment point cloud
    :param neighborhoods: list of neighborhoods which are themselves lists of indices referring to the environment
    :param target_point_cloud: point cloud of targets
    :param feature_names: list of features that are to be calculated
    :param volume: object describing the volume that contains the neighborhood points
    :param overwrite: if true, even features that are already in the targets point cloud will be calculated and stored
    :param kwargs: keyword arguments for the individual feature extractors
    :param verbose: if true, output extra information
    :return: None, results are stored in attributes of the target point cloud
    """
    _verify_feature_names(feature_names)
    wanted_feature_names = feature_names + [existing_feature for existing_feature in target_point_cloud[keys.point]]
    extended_features = _make_extended_feature_list(feature_names)
    features_to_do = extended_features

    while features_to_do:
        feature_name = features_to_do[0]

        if (target_idx_base == 0) and (not overwrite) and (feature_name in target_point_cloud[keys.point]):
            continue  # Skip feature calc if it is already there and we do not overwrite

        extractor = FEATURES[feature_name]

        if verbose:
            sys.stdout.write('Feature(s) "{}"'.format(extractor.provides()))
            sys.stdout.flush()
            start = time.time()

        _add_or_update_feature(env_point_cloud, neighborhoods, target_idx_base,
                               target_point_cloud, extractor, volume, overwrite, kwargs)
        utils.add_metadata(target_point_cloud, type(
            extractor).__module__, extractor.get_params())

        if verbose:
            elapsed = time.time() - start
            sys.stdout.write(' took {:.2f} seconds\n'.format(elapsed))
            sys.stdout.flush()

        for provided_feature in extractor.provides():
            if provided_feature in features_to_do:
                features_to_do.remove(provided_feature)

    _keep_only_wanted_features(target_point_cloud, wanted_feature_names)


def _keep_only_wanted_features(target_point_cloud, wanted_feature_names):
    redundant_features = [f for f in target_point_cloud[keys.point] if f not in wanted_feature_names]
    if redundant_features:
        print('The following unrequested features were calculated as a side effect, but will not be returned:',
              redundant_features)
    for f in redundant_features:
        target_point_cloud[keys.point].pop(f)


def _verify_feature_names(feature_names):
    unknown_features = [f for f in feature_names if f not in FEATURES]
    if any(unknown_features):
        raise ValueError('Unknown features selected: {}. Available feature are: {}'
                         .format(', '.join(unknown_features), ', '.join(FEATURES.keys())))


def _add_or_update_feature(env_point_cloud, neighborhoods, target_idx_base, target_point_cloud, extractor, volume,
                           overwrite, kwargs):
    n_targets = len(neighborhoods)

    for k in kwargs:
        setattr(extractor, k, kwargs[k])
    provided_features = extractor.provides()
    n_features = len(provided_features)
    feature_values = [np.empty(n_targets, dtype=np.float64)
                      for i in range(n_features)]

    if hasattr(extractor, 'is_vectorized'):
        _add_or_update_feature_in_chunks(env_point_cloud, extractor, feature_values, n_features, n_targets,
                                         neighborhoods,
                                         target_idx_base, target_point_cloud, volume)
    else:
        _add_or_update_feature_one_by_one(env_point_cloud, extractor, feature_values, n_features, n_targets,
                                          neighborhoods, target_idx_base, target_point_cloud, volume)

    for i in range(n_features):
        feature = provided_features[i]
        if target_idx_base != 0:
            if feature not in target_point_cloud[keys.point]:
                continue

            target_point_cloud[keys.point][feature]["data"] = np.hstack(
                [target_point_cloud[keys.point][feature]["data"], feature_values[i]])

        elif overwrite or (feature not in target_point_cloud[keys.point]):
            target_point_cloud[keys.point][feature] = {
                "type": 'float64', "data": feature_values[i]}


def _add_or_update_feature_one_by_one(env_point_cloud, extractor, feature_values, n_features, n_targets, neighborhoods,
                                      target_idx_base, target_point_cloud, volume):
    for target_index in range(n_targets):
        point_values = extractor.extract(env_point_cloud, neighborhoods[target_index], target_point_cloud,
                                         target_index + target_idx_base, volume)
        if n_features > 1:
            for i in range(n_features):
                feature_values[i][target_index] = point_values[i]
        else:
            feature_values[0][target_index] = point_values


def _add_or_update_feature_in_chunks(env_point_cloud, extractor, feature_values, n_features, n_targets, neighborhoods,
                                     target_idx_base, target_point_cloud, volume):
    chunk_size = 100000
    print('calculating {} in chunks'.format(extractor.provides()))
    for chunk_no in range(int(np.math.ceil(n_targets / chunk_size))):
        i_start = chunk_no * chunk_size
        i_end = min((chunk_no + 1) * chunk_size, n_targets)
        target_indices = np.arange(i_start, i_end)
        point_values = extractor.extract(env_point_cloud, neighborhoods[i_start:i_end], target_point_cloud,
                                         target_indices + target_idx_base, volume)

        if n_features > 1:
            for i in range(n_features):
                feature_values[i][target_indices] = point_values[i]
        else:
            feature_values[0][target_indices] = point_values


def _make_extended_feature_list(feature_names):
    feature_list = reversed(_make_extended_feature_list_helper(feature_names))
    return _remove_duplicates(feature_list)


def _remove_duplicates(feature_list):
    seen = set()
    return [f for f in feature_list if not (f in seen or seen.add(f))]


def _make_extended_feature_list_helper(feature_names):
    feature_list = feature_names
    for feature_name in feature_names:
        extractor = FEATURES[feature_name]
        dependencies = extractor.requires()
        feature_list.extend(dependencies)
        feature_list.extend(_make_extended_feature_list_helper(dependencies))
    return feature_list
