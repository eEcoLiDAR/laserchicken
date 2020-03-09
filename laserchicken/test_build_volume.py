from unittest import TestCase

from laserchicken.build_volume import VOLUMES, build_volume
from laserchicken.volume_specification import Cell, Cube, InfiniteCylinder, Sphere, Volume


_shapes = [Cell, Cube, InfiniteCylinder, Sphere]


class BuildVolumeTest(TestCase):
    def test_volume_not_in_volume_map(self):
        self.assertNotIn(Volume, VOLUMES.values())

    def test_elements_in_volume_map(self):
        for shape in _shapes:
            self.assertIn(shape.TYPE, VOLUMES.keys())
            self.assertIs(VOLUMES[shape.TYPE], shape)

    def test_missing_build_volume_arguments(self):
        with self.assertRaises(TypeError):
            vol = build_volume()

    def test_build_nonexistent_volume(self):
        with self.assertRaises(ValueError):
            vol = build_volume("test", radius=5)

    def test_wrong_keyword_argument(self):
        with self.assertRaises(TypeError):
            vol = build_volume("sphere", cell_length=5)
        with self.assertRaises(TypeError):
            vol = build_volume("cell", radius=5)

    def test_build_all_elements(self):
        param = 5
        for shape in _shapes:
            vol = build_volume(shape.TYPE, param)
            self.assertIsInstance(vol, shape)
            for attr, val in shape(param).__dict__.items():
                self.assertIn(attr, vol.__dict__)
                self.assertAlmostEqual(val, vol.__dict__[attr])
