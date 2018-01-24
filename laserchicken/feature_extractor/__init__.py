"""Feature extractor module."""
import importlib
import re
from laserchicken import keys


def _feature_map(module_name=__name__):
    """Construct a mapping from feature names to feature extractor classes."""
    module = importlib.import_module(module_name)
    return {
        feature_name: extractor
        for name, extractor in vars(module).items() if re.match('^[A-Z][a-zA-Z0-9_]*FeatureExtractor$', name)
        for feature_name in extractor.provides()
    }


FEATURES = _feature_map()


def compute_features(env_point_cloud, neighborhoods, target_point_cloud, feature_names):
    ordered_features = _make_feature_list(feature_names)
    for feature in ordered_features:
        if(feature in target_point_cloud): continue
        extractor = FEATURES[feature]()
        providedfeatures = extractor.provides()
        numfeatures = len(providedfeatures)
        featurevalues = [np.empty([target_indices],dtype = np.float64) for i in range(numfeatures)]
        for target_index in range(target_point_cloud[keys.point]["x"]["data"]):
            pointvalues = extractor.extract(env_point_cloud, neighborhoods[target_index], target_point_cloud, target_index)
            for f in numfeatures:
                featurevalues[f][target_index] = pointvalues[f]
        for i in range(numfeatures):
            if "features" not in target_point_cloud:
                target_point_cloud["features"] = {}
            fname = providedfeatures[i]
            target_point_cloud["features"][fname] = {"type" : np.float64, "data" : featurevalues[i]}


def _make_feature_list(feature_names):
    feature_list = reversed(_make_feature_list_helper(feature_names))
    seen = set()
    return [f for f in feature_list if not (f in seen or seen.add(f))]



def _make_feature_list_helper(feature_names):
    feature_list = feature_names
    for f in feature_names:
        extractor = FEATURES[feature_name]()
        dependencies = extractor.requires()
        feature_list.extend(dependencies)
        feature_list.extend(_make_feature_list_helper(dependencies))
    return feature_list
