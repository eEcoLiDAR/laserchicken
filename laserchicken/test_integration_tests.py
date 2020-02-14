import os
import unittest


class FromTutorial(unittest.TestCase):
    def test_tutorial_once(self):
        """This test should be identical to running all cells in the tutorial notebook once, in order."""
        from laserchicken import load
        point_cloud = load('testdata/AHN3.las')

        point_cloud

        from laserchicken.normalize import normalize
        normalize(point_cloud)

        point_cloud

        from laserchicken.filter import select_polygon
        polygon = "POLYGON(( 131963.984125 549718.375000," + \
                  " 132000.000125 549718.375000," + \
                  " 132000.000125 549797.063000," + \
                  " 131963.984125 549797.063000," + \
                  " 131963.984125 549718.375000))"
        point_cloud = select_polygon(point_cloud, polygon)

        from laserchicken.filter import select_above, select_below
        points_below_1_meter = select_below(point_cloud, 'normalized_height', 1)
        points_above_1_meter = select_above(point_cloud, 'normalized_height', 1)

        from laserchicken import compute_neighborhoods
        from laserchicken import build_volume
        targets = point_cloud
        volume = build_volume("sphere", radius=5)
        neighborhoods = compute_neighborhoods(point_cloud, targets, volume)

        from laserchicken import compute_features
        compute_features(point_cloud, neighborhoods, targets, ['std_z', 'mean_z', 'slope'], volume)

        from laserchicken import register_new_feature_extractor
        from laserchicken.feature_extractor.band_ratio_feature_extractor import BandRatioFeatureExtractor
        register_new_feature_extractor(BandRatioFeatureExtractor(None, 1, data_key='normalized_height'))
        register_new_feature_extractor(BandRatioFeatureExtractor(1, 2, data_key='normalized_height'))
        register_new_feature_extractor(BandRatioFeatureExtractor(2, None, data_key='normalized_height'))
        register_new_feature_extractor(BandRatioFeatureExtractor(None, 0, data_key='z'))

        from laserchicken.feature_extractor.feature_extraction import list_feature_names
        sorted(list_feature_names())

        cylinder = build_volume("infinite cylinder", radius=5)
        neighborhoods = compute_neighborhoods(point_cloud, targets, cylinder)
        compute_features(point_cloud, neighborhoods, targets, ['band_ratio_1<normalized_height<2'], cylinder)

        from laserchicken import export
        export(point_cloud, 'my_output.ply')

    def tearDown(self):
        os.remove('my_output.ply')