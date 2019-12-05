import numpy as np

from laserchicken.feature_extractor import FeatureExtractor


class FeatureExtractorAdaptor(FeatureExtractor):
    """Abstract feature extractor class."""

    def __init__(self, singular_extractor):
        self.singular_extractor = singular_extractor

    def requires(self):
        return self.singular_extractor.requires()

    def provides(self):
        return self.singular_extractor.provides()

    def extract(self, point_cloud, neighborhoods, targets, target_indices, volume_description):
        extractor = self.singular_extractor
        result = []
        for neighborhood, target_index in zip(neighborhoods, target_indices):
            result.append(extractor.extract(point_cloud, neighborhood, targets, target_index, volume_description))
        return np.array(result).T

    def get_params(self):
        return [self.singular_extractor.__module__] + list(self.singular_extractor.get_params())
