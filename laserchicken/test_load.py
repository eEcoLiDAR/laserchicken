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


    def test_load(self):
        """ Load module should call load_las to get the file. """
        nonexistent_las = 'nonexistent.las'
        nonexistent_ply = 'nonexistent.ply'
        with mock.patch('laserchicken.load_las.load') as load_las_mock:
            with mock.patch('laserchicken.write_ply.write') as write_ply_mock:
                load(nonexistent_las, nonexistent_ply)
                load_las_mock.assert_called_once_with(nonexistent_las)

    def test_write(self):
        """ Load module should call write_ply to get the file. """
        nonexistent_las = 'nonexistent.las'
        nonexistent_ply = 'nonexistent.ply'
        with mock.patch('laserchicken.write_ply.write') as write_ply_mock:
            with mock.patch('laserchicken.load_las.load') as load_las_mock:
                load(nonexistent_las, nonexistent_ply)
                write_ply_mock.assert_called_once_with(nonexistent_ply)
