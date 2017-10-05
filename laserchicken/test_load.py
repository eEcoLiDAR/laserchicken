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

    @mock.patch('laserchicken.load_las.load')
    def test_load(self, mock1):
        """ Should raise exception. """
        load('nonexistent.las')
        mock1.assert_called_once_with()
