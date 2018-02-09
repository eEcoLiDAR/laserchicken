import os
import random
import unittest


from laserchicken import keys, read_las, utils
from laserchicken.compute_neighbors import compute_cylinder_neighborhood_indices
from laserchicken.compute_neighbors import compute_sphere_neighborhood_indices
from laserchicken.compute_neighbors import compute_neighbourhoods
from laserchicken.volume_specification import Sphere, InfiniteCylinder
from laserchicken.feature_extractor.density_feature_extractor import PointDensityFeatureExtractor


class TestDensityFeatureExtractor(unittest.TestCase):

    _test_file_name = 'AHN3.las'
    _test_data_source = 'testdata'
    point_cloud = None

    def test_sphere_index(self):
        """Compute the density for a sphere given as index of the source pc."""
        neighbors_index = compute_sphere_neighborhood_indices(self.point_cloud,
                                                              self.targetpc,
                                                              self.sphere.radius)

        extractor = PointDensityFeatureExtractor()
        for index in neighbors_index:
            d = extractor.extract(self.point_cloud,index,None,None,self.sphere)


    def test_sphere_neighborhoods(self):
        """Compute the density for a sphere given as neighborhood."""
        neighborhood_pc = compute_neighbourhoods(self.point_cloud,self.targetpc,self.sphere)
        extractor = PointDensityFeatureExtractor()
        for pc in neighborhood_pc:
            d = extractor.extract(None,None,pc,None,self.sphere)


    def test_cylinder_index(self):
        """Compute the density for a cylinder given as index of source pc."""
        neighbors_index = compute_cylinder_neighborhood_indices(self.point_cloud,
                                                                self.targetpc,
                                                                self.cyl.radius)
        extractor = PointDensityFeatureExtractor()
        for index in neighbors_index:
            d = extractor.extract(self.point_cloud,index,None,None,self.cyl)

    def test_cylinder_neighborhoods(self):
        """Compute the density for a cylinder given as neighborhood."""
        neighborhood_pc = compute_neighbourhoods(self.point_cloud,self.targetpc,self.cyl)
        extractor = PointDensityFeatureExtractor()
        for pc in neighborhood_pc:
            d = extractor.extract(None,None,pc,None,self.cyl)

    def _get_random_targets(self):
        num_all_pc_points = len(self.point_cloud[keys.point]["x"]["data"])
        rand_indices = [random.randint(0, num_all_pc_points) for p in range(20)]
        return utils.copy_pointcloud(self.point_cloud, rand_indices)

    def setUp(self):
        self.point_cloud = read_las.read(os.path.join(self._test_data_source, self._test_file_name))

        random.seed(102938482634)
        self.targetpc = self._get_random_targets()

        radius = 0.5
        self.sphere = Sphere(radius)
        self.cyl = InfiniteCylinder(radius)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()