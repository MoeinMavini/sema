import os
import sys
from setuptools import setup

if sys.version_info[0] != 3:
    sys.stderr.write("Python version '3' is required")
    sys.exit(1)

setup(packages=['command_line', 'common'],
      py_modules = ['sema'])

