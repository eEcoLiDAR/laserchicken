import os
import unittest

from distutils.version import StrictVersion

import laserchicken

class TestVersion(unittest.TestCase):
    version_file_path = None

    def test_version_file_exists(self):
        self.assertTrue(os.path.isfile(self.version_file_path))

    def test_version_file_is_readable(self):
        with open(self.version_file_path) as f:
            readable = f.readable()
        self.assertTrue(readable)

    def test_version_file_is_not_empty(self):
        self.assertTrue(self._read_version(self.version_file_path))

    def test_version_is_correct(self):
        version_read = StrictVersion(self._read_version(self.version_file_path))
        verson_import = laserchicken.__version__
        self.assertEqual(version_read, verson_import)

    @staticmethod
    def _read_version(file_path):
        with open(file_path) as f:
            lines = f.read()
        return lines.strip()

    def setUp(self):
        cwd = os.path.dirname(__file__)
        self.version_file_path = os.path.join(cwd, '_version.txt')