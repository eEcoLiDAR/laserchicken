import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'laserchicken/_version.py')) as versionpy:
    exec(versionpy.read())


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='laserchicken',
    version=__version__,
    description='Point cloud toolkit',
    license='Apache 2.0',
    keywords=['Python', 'Point cloud'],
    url='https://github.com/eEcoLiDAR/eEcoLiDAR',
    packages=['laserchicken'],
    install_requires=required,
    long_description=read('README.md'),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'laserchicken = laserchicken.tools.cli:main',
        ],
    },
)
