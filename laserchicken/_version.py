import os

with open(os.path.join(os.path.dirname(__file__), '_version.txt'),
          'r') as f:
    version = f.read()
__version__ = version.strip()
