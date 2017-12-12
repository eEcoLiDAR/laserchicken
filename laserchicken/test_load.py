import os
import sys
import unittest

from laserchicken.load import load

if sys.version_info.major == 2:
    import mock
else:
    from unittest import mock


class TestLoad(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = '5points.las'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    @mock.patch('laserchicken.write_ply.write')
    @mock.patch('laserchicken.read_las.read')
    def test_load(self, load_las_mock, write_ply_mock):
        """ Load module should call load_las to get the file. """
        nonexistent_las = 'nonexistent.las'
        nonexistent_ply = 'nonexistent.ply'
        load(nonexistent_las, nonexistent_ply)
        load_las_mock.assert_called_once_with(nonexistent_las)

    @unittest.skip('Production code not implemented yet.')
    @mock.patch('laserchicken.write_ply.write')
    @mock.patch('laserchicken.read_las.read')
    def test_write(self, load_las_mock, write_ply_mock):
        """ Load module should call write_ply to get the file. """
        nonexistent_las = 'nonexistent.las'
        nonexistent_ply = 'nonexistent.ply'
        load(nonexistent_las, nonexistent_ply)
        write_ply_mock.assert_called_once_with(nonexistent_ply)
