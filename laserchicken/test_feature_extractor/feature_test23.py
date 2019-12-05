"""Test2 and Test3 feature extractors."""
import numpy as np

from laserchicken import utils
from laserchicken.feature_extractor.base_feature_extractor import FeatureExtractor


class Test2FeatureExtractor(FeatureExtractor):
    @classmethod
    def requires(cls):
        return ['test1_b']

    @classmethod
    def provides(cls):
        return ['test2_a', 'test2_b', 'test2_c']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        t1b = utils.get_attribute_value(targetpc, targetindex, self.requires()[0])
        x, y, z = utils.get_point(targetpc, targetindex)
        return [x + t1b, y + t1b, z + t1b]  # x + 3z/2, y + 3z/2, 5z/2


class Test3FeatureExtractor(FeatureExtractor):
    @classmethod
    def requires(cls):
        return ['test1_a', 'test2_c']

    @classmethod
    def provides(cls):
        return ['test3_a']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        t2a, t2c = utils.get_features(targetpc, self.requires(), targetindex)
        x, y, z = utils.get_point(targetpc, targetindex)
        return t2c - t2a - z  # z


class TestVectorizedFeatureExtractor(FeatureExtractor):
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['vectorized1', 'vectorized2']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume):
        x = utils.get_features(targetpc, ['x'], targetindex)
        x1 = np.array(list(x))[0]
        return x1, x1
