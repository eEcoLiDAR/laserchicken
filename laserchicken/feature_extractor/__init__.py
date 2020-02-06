from laserchicken.feature_extractor.feature_map import create_default_feature_map, _create_name_extractor_pairs
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor

FEATURES = create_default_feature_map()


def list_feature_names():
    return FEATURES#[feature_name for feature_name in FEATURES]


def register_new_feature_extractor(extractor: FeatureExtractor):
    for name, extractor in _create_name_extractor_pairs([extractor]):
        FEATURES[name] = extractor
