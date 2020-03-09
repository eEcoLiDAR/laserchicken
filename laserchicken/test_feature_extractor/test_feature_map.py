"""Test that the map from feature names to extractor classes is correct."""
import unittest

from laserchicken.feature_extractor import feature_extraction
from laserchicken.test_feature_extractor import Test1FeatureExtractor


class FeatureMapTests(unittest.TestCase):

    def test__feature_map(self):
        expected_features = ['point_density', 'echo_ratio', 'eigenv_1', 'eigenv_2', 'eigenv_3', 'normal_vector_1',
                             'normal_vector_2', 'normal_vector_3', 'slope', 'entropy_z', 'pulse_penetration_ratio',
                             'sigma_z', 'median_z', 'max_z', 'min_z',
                             'range_z', 'var_z', 'mean_z', 'std_z', 'coeff_var_z', 'skew_z', 'kurto_z', 'skew_normalized_height',
                             'mean_normalized_height','std_normalized_height', 'coeff_var_normalized_height', 'var_normalized_height', 'min_normalized_height',
                             'max_normalized_height', 'range_normalized_height', 'kurto_normalized_height', 'entropy_normalized_height',
                             'median_normalized_height', 'max_intensity',
                             'density_absolute_mean_z', 'density_absolute_mean_normalized_height', 'perc_15_z',
                             'perc_99_normalized_height', 'max_intensity', 'min_intensity', 'range_intensity', 'mean_intensity', 'std_intensity', 'coeff_var_intensity']
        for feature in expected_features:
            self.assertIn(feature, feature_extraction.FEATURES)

    def test_feature_map_contains_new_feature_after_registration(self):
        test_feature_extractor = Test1FeatureExtractor()
        expected_features = test_feature_extractor.provides()

        feature_extraction.register_new_feature_extractor(test_feature_extractor)

        for feature in expected_features:
            self.assertIn(feature, feature_extraction.FEATURES)

    def test_list_all_feature_names_contains_items(self):
        names = feature_extraction.list_feature_names()
        self.assertGreater(len(names), 0)

    def test_list_all_feature_names_are_strings(self):
        names = feature_extraction.list_feature_names()
        for name in names:
            self.assertEqual(type(name), str)
