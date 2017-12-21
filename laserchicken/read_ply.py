import os
import shutil
import unittest
import numpy as np

from pytest import raises


def read(path):
    if not os.path.exists(path):
        raise FileNotFoundError('File not found: {}'.format(path))

    with open(path, 'r') as ply:
        try:
            first_line = ply.readline()
        except UnicodeDecodeError:
            first_line = ''

        if 'ply' not in first_line:
            raise ValueError('Not a valid ply file: {}'.format(path))

        for line in ply:
            index = []
            element_type = 'vertex'
            element_vertex_ = 'element {} '.format(element_type)
            if element_vertex_ in line:
                number_of_elements = int(line.split(element_vertex_)[1])
                index.append({'type': element_type, 'number_of_elements': number_of_elements})

            return [[None for i in range(element_block['number_of_elements'])] for element_block in index]


class TestReadPly(unittest.TestCase):
    _test_dir = 'TestLoad_dir'
    _test_file_name = 'example.ply'
    _las_file_name = '5points.las'
    _test_data_source = 'testdata'
    las_file_path = os.path.join(_test_dir, _las_file_name)
    test_file_path = os.path.join(_test_dir, _test_file_name)

    def test_unexistentFile_error(self):
        with raises(OSError):
            read('nonexistentfile.ply')

    def test_wrongFormat_error(self):
        with raises(ValueError):
            read(self.las_file_path)

    def test_existentPly_noError(self):
        read(self.test_file_path)

    def test_containsPointsElement(self):
        data = read(self.test_file_path)
        self.assertIn('points', data)

    def test_rightNumberOfPoints(self):
        data = read(self.test_file_path)
        self.assertEqual(len(data['points']), 3)

    def test_correctPoints(self):
        data = read(self.test_file_path)
        np.testing.assert_allclose(data['points'][0]['data'], np.array([0.11, 0.12, 0.13, 1]))

    def setUp(self):
        os.mkdir(self._test_dir)
        shutil.copyfile(os.path.join(self._test_data_source, self._test_file_name), self.test_file_path)
        shutil.copyfile(os.path.join(self._test_data_source, self._las_file_name), self.las_file_path)

    def tearDown(self):
        shutil.rmtree(self._test_dir)
