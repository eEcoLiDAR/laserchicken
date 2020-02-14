import os

from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


required = read('requirements.txt').splitlines()
version = read('laserchicken/_version.txt').strip()


setup(
    name='laserchicken',
    version=version,
    description='Point cloud toolkit',
    license='Apache 2.0',
    keywords=['Python', 'Point cloud'],
    url='https://github.com/eEcoLiDAR/eEcoLiDAR',
    packages=find_packages(),
    install_requires=required,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'laserchicken = laserchicken.tools.cli:main',
        ],
    },
    package_data={'': ['_version.txt']},
)
