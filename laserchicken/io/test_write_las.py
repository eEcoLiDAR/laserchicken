import os
import shutil
import unittest

import laspy
import numpy as np
import pytest

from laserchicken import keys
from laserchicken.test_tools import SimpleTestData, ComplexTestData
from laserchicken.test_tools import create_point_cloud
from laserchicken.io.export import export
from laserchicken.io.load import load
from laserchicken.io.las_handler import is_pylas_available

@pytest.mark.skipif(not is_pylas_available, reason="requires pylas for writing")
class TestWriteLas(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'test.las'
    _test_data_source = 'testdata'
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_write_emptyData(self):
        """ Should raise an exception """
        pc = create_point_cloud([], [], [])
        with pytest.raises(ValueError):
            export(pc, self.test_file_path)

    def test_write_nonExistentDir(self):
        """ Should raise an exception """
        pc = SimpleTestData.get_point_cloud()
        with pytest.raises(FileNotFoundError):
            export(pc, os.path.join('/nonexistentdir', self._test_file_name))

    def test_write_sameFileTwice(self):
        """ Should raise an exception """
        pc = SimpleTestData.get_point_cloud()
        export(pc, self.test_file_path)
        with pytest.raises(FileExistsError):
            export(pc, self.test_file_path)

    def test_write_sameFileTwiceOverwrite(self):
        """ Should not raise an exception """
        pc = SimpleTestData.get_point_cloud()
        export(pc, self.test_file_path)
        export(pc, self.test_file_path, overwrite=True)
        self.assertTrue(os.path.isfile(self.test_file_path))

    def test_write_loadTheSameSimpleData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        pc = SimpleTestData.get_point_cloud()
        export(pc, self.test_file_path)
        file = _get_file_from_path(self.test_file_path)
        _assert_all_attributes_in_file(pc[keys.point], file)

    def test_write_loadTheSameComplexData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        test_data = ComplexTestData()
        pc = test_data.get_point_cloud()
        export(pc, self.test_file_path)
        file = _get_file_from_path(self.test_file_path)
        _assert_all_attributes_in_file(pc[keys.point], file)

    def test_write_loadRealData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        pc = load(os.path.join(self._test_data_source, 'AHN3.las'))
        export(pc, self.test_file_path)
        file = _get_file_from_path(self.test_file_path)
        _assert_all_attributes_in_file(pc[keys.point], file)

    def test_write_processedRealData(self):
        """ Writing point cloud data and loading it afterwards should result in the same point cloud data. """
        pc = load(os.path.join(self._test_data_source, 'AHN3.las'))
        x = pc[keys.point]['x']['data']
        pc[keys.point]['test_feature'] = {'data': np.zeros_like(x), 'type': 'float64'}
        export(pc, self.test_file_path)
        file = _get_file_from_path(self.test_file_path)
        _assert_all_attributes_in_file(pc[keys.point], file)

    def setUp(self):
        os.mkdir(self._test_dir)

    def tearDown(self):
        shutil.rmtree(self._test_dir)


def _assert_all_attributes_in_file(attributes, file):
    for name, attribute in attributes.items():
        data = attribute['data']
        dtype = np.dtype(attribute['type'])
        assert hasattr(file, name)
        file_data = getattr(file, name)
        assert dtype.name == file_data.dtype.name
        assert data.size == file_data.size
        np.testing.assert_allclose(data, file_data, err_msg="{} differ".format(name))


def _get_file_from_path(path):
    return laspy.file.File(path)
