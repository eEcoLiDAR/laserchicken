import numpy as np
import unittest
from laserchicken import keys,utils
from laserchicken.feature_extractor.normal_plane_feature_extractor import NormalPlaneFeatureExtractor


class TestNormalPlaneFeatureExtractor(unittest.TestCase):

    pc = None
    neighborhood = None
    nvect = None

    def test_normal_plane(self):

        extractor = NormalPlaneFeatureExtractor()
        nfit = extractor.extract(self.pc,self.neighborhood,None,None,None)
        self.assertTrue(np.allclose(self.nvect,nfit))

    def setUp(self):
        self.nvect = np.array([1.,2.,3.])
        self.nvect /= np.linalg.norm(self.nvect)
        x,y,z = utils.generate_random_points_inplane(self.nvect,npts=10)
        self.pc = {keys.point: {'x': {'type': 'double', 'data': x},
                           'y': {'type': 'double', 'data': y},
                           'z': {'type': 'double', 'data': z}}}
        self.neighborhood = [3,4,5,6,7]

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()