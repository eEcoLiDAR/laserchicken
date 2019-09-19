import os
import shutil
import unittest

import pytest

from laserchicken.test_tools import SimpleTestData, ComplexTestData
from laserchicken.write_ply import write
from laserchicken.read_ply import read

import numpy as np


def read_header(ply):
    header = ''
    line = ply.readline()
    while line.strip() != 'end_header':
        header = header + line
        line = ply.readline()
    return header


def read_data(ply):
    data = ''
    in_header = True
    for line in ply:
        if line == 'end_header\n':
            in_header = False
        else:
            if not in_header:
                data = data + line
    return data


class TestWritePly(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'test.ply'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_write_nonExistingFile(self):
        """ Should create a file. """
        pc = SimpleTestData.get_point_cloud()
        write(pc, self.test_file_path)
        assert (os.path.exists(self.test_file_path))

    def test_write_sameFileTwice(self):
        """ Should throw an exception. """
        pc = SimpleTestData.get_point_cloud()
        write(pc, self.test_file_path)
        # Catch most specific subclass of FileExistsError (3.6) and IOError (2.7).
        with pytest.raises(Exception):
            write(pc, self.test_file_path)

    def test_write_loadTheSameSimpleData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        pc_in = SimpleTestData.get_point_cloud()
        write(pc_in, self.test_file_path)
        data_in = SimpleTestData.get_data()
        with open(self.test_file_path, 'r') as ply:
            data_out = read_data(ply)
        self.assertEqual(data_in, data_out)

    def test_write_loadTheSameComplexData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        test_data = ComplexTestData()
        pc_in = test_data.get_point_cloud()
        write(pc_in, self.test_file_path)
        data_in = test_data.get_data()
        with open(self.test_file_path, 'r') as ply:
            data_out = read_data(ply)
        self.assertEqual(data_in, data_out)

    def test_write_and_read_sanity_check(self):
        """ Writing point cloud loading it afterwards should result in same point cloud. """
        original_point_cloud = ComplexTestData().get_point_cloud()
        write(original_point_cloud, self.test_file_path)

        read_point_cloud = read(self.test_file_path)

        self._assert_nested_structure_equal(original_point_cloud, read_point_cloud)

    def _assert_nested_structure_equal(self, a, b):
        if type(a) == list:
            for element_in_a, element_in_b in zip(a, b):
                self._assert_nested_structure_equal(element_in_a, element_in_b)
        elif type(a) == dict:
            for key in a:
                if key in b:
                    print(key, a, b)
                    value_in_a = a[key]
                    value_in_b = b[key]
                    self._assert_nested_structure_equal(value_in_a, value_in_b)
                else:
                    raise AssertionError(key)
        elif type(a) == np.ndarray:
            np.testing.assert_allclose(a, b)
        else:
            print(a, b, type(a), type(b))
            self.assertEqual(a, b)

    def setUp(self):
        os.mkdir(self._test_dir)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
