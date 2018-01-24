"""Test1 feature extractor."""
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor


class Test1FeatureExtractor(AbstractFeatureExtractor):
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['test1_a', 'test1_b']

    def extract(self, _, target):
        for feature_name in self.provides():
            if feature_name not in target:
                target[feature_name] = len(target)
