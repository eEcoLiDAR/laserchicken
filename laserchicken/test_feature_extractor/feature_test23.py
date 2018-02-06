"""Test2 and Test3 feature extractors."""
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken import utils


class Test2FeatureExtractor(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return ['test1_b']

    @classmethod
    def provides(cls):
        return ['test2_a', 'test2_b', 'test2_c']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        t1b = utils.get_feature(targetpc, targetindex, self.requires()[0])
        x, y, z = utils.get_point(targetpc, targetindex)
        return [x + t1b, y + t1b, z + t1b]  # x + 3z/2, y + 3z/2, 5z/2


class Test3FeatureExtractor(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return ['test1_a', 'test2_c']

    @classmethod
    def provides(cls):
        return ['test3_a']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        t2a, t2c = utils.get_features(targetpc, targetindex, self.requires())
        x, y, z = utils.get_point(targetpc, targetindex)
        return t2c - t2a - z  # z
