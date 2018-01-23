"""Feature extractor module."""
import importlib
import re


def _feature_map(module_name=__name__):
    """Construct a mapping from feature names to feature extractor classes."""
    module = importlib.import_module(module_name)
    return {
        feature_name: extractor
        for name, extractor in vars(module).items() if re.match('^[A-Z][a-zA-Z0-9_]*FeatureExtractor$', name)
        for feature_name in extractor.provides()
    }


FEATURES = _feature_map()


def extract_features(point_cloud, target, feature_names):
    """Add features to a given target using point_cloud."""
    for feature_name in feature_names:
        if feature_name in target:
            continue

        extractor = FEATURES[feature_name]()
        extract_features(point_cloud, target, extractor.requires())
        extractor.extract(point_cloud, target)
        assert feature_name in target, ("{} failed to add feature {} to target {}".format(
            type(extractor).__name__, feature_name, target))
