"""Test1 feature extractor."""
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor
from laserchicken import utils


class Test1FeatureExtractor(FeatureExtractor):
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['test1_a', 'test1_b']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        x, y, z = utils.get_point(targetpc, targetindex)
        return [0.5 * z, 1.5 * z]
