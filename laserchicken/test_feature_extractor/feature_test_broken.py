"""Broken feature extractor."""
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor


class TestBrokenFeatureExtractor(FeatureExtractor):
    """Feature extractor that fails to add the feature in promises to provide to target."""

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['test_broken']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        pass
