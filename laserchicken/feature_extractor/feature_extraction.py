"""Feature extractor module."""
import copy
import itertools
import sys
import time

import numpy as np

from laserchicken import utils
from laserchicken.keys import point, provenance
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken.feature_extractor.feature_map import create_default_feature_map, _create_name_extractor_pairs

FEATURES = create_default_feature_map()


def list_feature_names():
    return FEATURES  # [feature_name for feature_name in FEATURES]


def register_new_feature_extractor(extractor: FeatureExtractor):
    for name, extractor in _create_name_extractor_pairs([extractor]):
        FEATURES[name] = extractor


def compute_features(env_point_cloud, neighborhoods, target_point_cloud, feature_names, volume, verbose=True, **kwargs):
    """
    Compute features for each target and store result as point attributes in target point cloud.

    Example:
    >>> point_cloud = load('data1.ply')
    >>> target_point_cloud = load('data2.ply')
    >>> volume = build_volume('infinite cylinder', radius=4)
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
    :param kwargs: keyword arguments for the individual feature extractors
    :param verbose: if true, output extra information
    :return: None, results are stored in attributes of the target point cloud
    """
    _verify_feature_names(feature_names)
    wanted_feature_names = feature_names + [existing_feature for existing_feature in target_point_cloud[point]]
    extended_features = _make_extended_feature_list(feature_names)

    for feature_name in extended_features:
        target_point_cloud[point][feature_name] = {"type": 'float64',
                                                   "data": np.zeros_like(target_point_cloud[point]['x']['data'],
                                                                         dtype=np.float64)}

    if provenance in env_point_cloud:
        utils.add_metadata(target_point_cloud, sys.modules[__name__],
                           {'env_point_cloud': {provenance: copy.copy(env_point_cloud[provenance])}})

    _add_features(extended_features, env_point_cloud, neighborhoods, target_point_cloud, volume, verbose, kwargs)

    _keep_only_wanted_features(target_point_cloud, wanted_feature_names)


def _add_features(extended_features, env_point_cloud, neighborhoods, target_point_cloud, volume, verbose, kwargs):
    chunk_size = 100000
    n_targets = _get_point_cloud_size(target_point_cloud)
    for chunk_no in range(_calculate_number_of_chunks(chunk_size, n_targets)):
        i_start = chunk_no * chunk_size
        i_end = min((chunk_no + 1) * chunk_size, n_targets)
        target_indices = np.arange(i_start, i_end)
        current_neighborhoods = list(itertools.islice(neighborhoods, i_end - i_start))

        features_to_do = list(extended_features)

        _compute_features_for_chunk(features_to_do, env_point_cloud, current_neighborhoods, target_point_cloud,
                                    target_indices, volume, verbose, kwargs)


def _get_point_cloud_size(target_point_cloud):
    return len(target_point_cloud[point]['x']['data'])


def _calculate_number_of_chunks(chunk_size, n_targets):
    return int(np.math.ceil(n_targets / chunk_size))


def _compute_features_for_chunk(features_to_do, env_point_cloud, current_neighborhoods, target_point_cloud,
                                target_indices, volume,
                                verbose, kwargs):
    while features_to_do:
        feature_name = features_to_do[0]
        extractor = FEATURES[feature_name]

        if verbose:
            sys.stdout.write('Extracting feature(s) "{}"'.format(extractor.provides()))
            start = time.time()

        for key_word in kwargs:
            setattr(extractor, key_word, kwargs[key_word])
        _add_features_from_single_extractor(extractor, env_point_cloud, current_neighborhoods, target_point_cloud,
                                            target_indices, volume)
        utils.add_metadata(target_point_cloud, type(extractor).__module__, extractor.get_params())

        if verbose:
            elapsed = time.time() - start
            sys.stdout.write('Extracting feature(s) "{}" took {:.2f} seconds\n'.format(extractor.provides(), elapsed))

        for provided_feature in extractor.provides():
            if provided_feature in features_to_do:
                features_to_do.remove(provided_feature)


def _add_features_from_single_extractor(extractor, env_point_cloud, current_neighborhoods, target_point_cloud,
                                        target_indices, volume):
    provided_features = extractor.provides()
    n_features = len(provided_features)
    point_values = extractor.extract(env_point_cloud, current_neighborhoods, target_point_cloud,
                                     target_indices, volume)

    n_targets = len(target_indices)
    feature_values = [np.empty(n_targets, dtype=np.float64) for _ in range(n_features)]
    if n_features > 1:
        for i in range(n_features):
            feature_values[i] = point_values[i]
    else:
        feature_values[0] = point_values
    for i in range(n_features):
        feature = provided_features[i]
        target_point_cloud[point][feature]['data'][target_indices] = feature_values[i]


def _keep_only_wanted_features(target_point_cloud, wanted_feature_names):
    redundant_features = [f for f in target_point_cloud[point] if f not in wanted_feature_names]
    if redundant_features:
        print('The following unrequested features were calculated as a side effect, but will not be returned:',
              redundant_features)
    for f in redundant_features:
        target_point_cloud[point].pop(f)


def _verify_feature_names(feature_names):
    unknown_features = [f for f in feature_names if f not in FEATURES]
    if any(unknown_features):
        raise ValueError('Unknown features selected: {}. Available feature are: {}'
                         .format(', '.join(unknown_features), ', '.join(FEATURES.keys())))


def _make_extended_feature_list(feature_names):
    feature_list = reversed(_make_extended_feature_list_helper(feature_names))
    return _remove_duplicates(feature_list)


def _remove_duplicates(feature_list):
    seen = set()
    return [f for f in feature_list if not (f in seen or seen.add(f))]


def _make_extended_feature_list_helper(feature_names):
    feature_list = list(feature_names)
    for feature_name in feature_names:
        extractor = FEATURES[feature_name]
        dependencies = extractor.requires()
        feature_list.extend(dependencies)
        feature_list.extend(_make_extended_feature_list_helper(dependencies))
        feature_list.extend(extractor.provides())
    return feature_list
