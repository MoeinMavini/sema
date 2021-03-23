import os
import sys
from setuptools import setup

if sys.version_info[0] != 3:
    sys.stderr.write("Python version '3' is required")
    sys.exit(1)

setup(
    package_dir = { 'sema': 'sema',
                    'sema.common': 'sema/common',
                    'sema.manage_setting': 'sema/manage_setting'},

    packages=['sema', 'sema.common', 'sema.manage_setting'],

    py_modules = [],

    entry_points = {"console_scripts": [ "sema = sema.sema_cl_nav:main" ]})

