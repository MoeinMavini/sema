import os
import sys
from setuptools import setup

if sys.version_info[0] != 3:
    sys.stderr.write("Python version '3' is required")
    sys.exit(1)

setup(packages=['Command_Line'],
      py_modules = ['sema'])

