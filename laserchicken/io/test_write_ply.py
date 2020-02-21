import os
import shutil
import unittest

import pytest

from laserchicken.test_tools import SimpleTestData, ComplexTestData
from laserchicken.io.export import export


def read_header(ply, is_binary=False):
    header = ''
    line = ply.readline()
    if is_binary: line = line.decode("utf-8")
    while line.strip() != 'end_header':
        header = header + line
        line = ply.readline()
        if is_binary: line = line.decode("utf-8")
    return header


def read_data_ascii(ply):
    data = ''
    in_header = True
    for line in ply:
        if line == 'end_header\n':
            in_header = False
        else:
            if not in_header:
                data = data + line
    return data


def read_data_binary(ply):
    data = b''
    in_header = True
    for line in ply:
        if in_header:
            if line.decode('utf-8') == 'end_header\n':
                in_header = False
        else:
            if not in_header:
                data = data + line.rstrip()
    return data


class TestWritePly(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'test.ply'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_write_nonExistingFile(self):
        """ Should create a file. """
        pc = SimpleTestData.get_point_cloud()
        export(pc, self.test_file_path)
        assert (os.path.exists(self.test_file_path))

    def test_write_sameFileTwice(self):
        """ Should throw an exception. """
        pc = SimpleTestData.get_point_cloud()
        export(pc, self.test_file_path)
        # Catch most specific subclass of FileExistsError (3.6) and IOError (2.7).
        with pytest.raises(Exception):
            export(pc, self.test_file_path)

    def test_write_sameFileTwiceOverwrite(self):
        """ Should not raise an exception """
        pc = SimpleTestData.get_point_cloud()
        export(pc, self.test_file_path)
        export(pc, self.test_file_path, overwrite=True)
        self.assertTrue(os.path.isfile(self.test_file_path))

    def test_write_invalidAttributes(self):
        """ Should raise exception. """
        test_data = ComplexTestData()
        pc = test_data.get_point_cloud()
        with pytest.raises(ValueError):
            export(pc, self.test_file_path, attributes=None)
        with pytest.raises(ValueError):
            export(pc, self.test_file_path, attributes=['ytisnetni'])

    def test_write_loadTheSameSimpleHeader(self):
        """  Writing a simple point cloud and loading it afterwards should result in the same point cloud."""
        pc_in = SimpleTestData.get_point_cloud()
        header_in = SimpleTestData.get_header()
        export(pc_in, self.test_file_path)
        with open(self.test_file_path, 'r') as ply:
            header_out = read_header(ply)
        self.assertMultiLineEqual(header_in, header_out)

    def test_write_loadTheSameComplexHeader(self):
        """  Writing a complex point cloud and loading it afterwards should result in the same point cloud."""
        test_data = ComplexTestData()
        pc_in = test_data.get_point_cloud()
        header_in = test_data.get_header()
        export(pc_in, self.test_file_path)
        with open(self.test_file_path, 'r') as ply:
            header_out = read_header(ply)
        self.assertMultiLineEqual(header_in, header_out)

    def test_write_loadTheSameSimpleData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        pc_in = SimpleTestData.get_point_cloud()
        export(pc_in, self.test_file_path)
        data_in = SimpleTestData.get_data()
        with open(self.test_file_path, 'r') as ply:
            data_out = read_data_ascii(ply)
        self.assertEqual(data_in, data_out)

    def test_write_loadTheSameComplexData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        test_data = ComplexTestData()
        pc_in = test_data.get_point_cloud()
        export(pc_in, self.test_file_path)
        data_in = test_data.get_data()
        with open(self.test_file_path, 'r') as ply:
            data_out = read_data_ascii(ply)
        self.assertEqual(data_in, data_out)

    def test_write_loadTheSameSimpleHeaderBinary(self):
        """  Writing a simple point cloud and loading it afterwards should result in the same point cloud."""
        pc_in = SimpleTestData.get_point_cloud()
        header_in = SimpleTestData.get_header(is_binary=True)
        export(pc_in, self.test_file_path, is_binary=True)
        with open(self.test_file_path, 'rb') as ply:
            header_out = read_header(ply, is_binary=True)
        self.assertMultiLineEqual(header_in, header_out)

    def test_write_loadTheSameSimpleDataBinary(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        pc_in = SimpleTestData.get_point_cloud()
        export(pc_in, self.test_file_path, is_binary=True)
        data_in = SimpleTestData.get_data(is_binary=True)
        with open(self.test_file_path, 'rb') as ply:
            data_out = read_data_binary(ply)
        self.assertEqual(data_in, data_out)

    def test_write_loadTheSameComplexHeaderBinary(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        test_data = ComplexTestData()
        pc_in = test_data.get_point_cloud()
        header_in = test_data.get_header(is_binary=True)
        export(pc_in, self.test_file_path, is_binary=True)
        with open(self.test_file_path, 'rb') as ply:
            header_out = read_header(ply, is_binary=True)
        self.assertEqual(header_in, header_out)

    def test_write_loadTheSameComplexDataBinary(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        test_data = ComplexTestData()
        pc_in = test_data.get_point_cloud()
        data_in = test_data.get_data(is_binary=True)
        export(pc_in, self.test_file_path, is_binary=True)
        with open(self.test_file_path, 'rb') as ply:
            data_out = read_data_binary(ply)
        self.assertEqual(data_in, data_out)

    def setUp(self):
        os.mkdir(self._test_dir)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
