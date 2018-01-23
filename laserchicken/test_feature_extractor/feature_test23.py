"""Test2 and Test3 feature extractors."""
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor


class Test2FeatureExtractor(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return ['test1_b']

    @classmethod
    def provides(cls):
        return ['test2_a', 'test2_b', 'test2_c']

    def extract(self, _, target):
        for feature_name in self.provides():
            target[feature_name] = len(target)


class Test3FeatureExtractor(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return ['test1_a', 'test2_c']

    @classmethod
    def provides(cls):
        return ['test3_a']

    def extract(self, _, target):
        for feature_name in self.provides():
            target[feature_name] = len(target)
