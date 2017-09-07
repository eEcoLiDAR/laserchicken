import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'mcfly/_version.py')) as versionpy:
    exec(versionpy.read())

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "temp",
    version = __version__,
    description = ("Point cloud toolkit"),
    license = "Apache 2.0",
    keywords = "Python", "Point cloud"
    url = "https://github.com/NLeSC/mcfly",
    packages=[],
    install_requires=required,
    long_description=read('README.md'),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
)
