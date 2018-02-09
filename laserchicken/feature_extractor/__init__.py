"""Feature extractor module."""
import importlib
import itertools
import re
import numpy as np
from laserchicken import keys, utils
from .entropy_feature_extractor import EntropyFeatureExtractor
from .eigenvals_feature_extractor import EigenValueFeatureExtractor
from .percentile_feature_extractor import PercentileFeatureExtractor

def _feature_map(module_name=__name__):
    """Construct a mapping from feature names to feature extractor classes."""
    module = importlib.import_module(module_name)
    return {
        feature_name: extractor
        for name, extractor in vars(module).items() if re.match('^[A-Z][a-zA-Z0-9_]*FeatureExtractor$', name)
        for feature_name in extractor.provides()
    }


FEATURES = _feature_map()


def compute_features(env_point_cloud, neighborhoods, target_point_cloud, feature_names, overwrite = False, **kwargs):
    ordered_features = _make_feature_list(feature_names)
    targetsize = len(target_point_cloud[keys.point]["x"]["data"])
    for feature in ordered_features:
        if ((not overwrite) and (feature in target_point_cloud[keys.point])):
            continue  # Skip feature calc if it is already there and we do not overwrite
        extractor = FEATURES[feature]()
        for k in kwargs:
            setattr(extractor,k,kwargs[k])
        providedfeatures = extractor.provides()
        numfeatures = len(providedfeatures)
        featurevalues = [np.empty(targetsize, dtype=np.float64) for i in range(numfeatures)]
        for target_index in range(targetsize):
            pointvalues = extractor.extract(env_point_cloud, neighborhoods[target_index], target_point_cloud,
                                            target_index)
            if numfeatures > 1:
                for i in range(numfeatures):
                    featurevalues[i][target_index] = pointvalues[i]
            else:
                featurevalues[0][target_index] = pointvalues
        for i in range(numfeatures):
            fname = providedfeatures[i]
            if (overwrite or (fname not in target_point_cloud[keys.point])):
                # Set feature values if it is not there (or we want to overwrite)
                target_point_cloud[keys.point][fname] = {"type": np.float64, "data": featurevalues[i]}
        utils.add_metadata(target_point_cloud, type(extractor).__module__, extractor.get_params())


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
