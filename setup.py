#!/usr/bin/env python

import setuptools
from distutils.core import setup, Extension
from setupext import ext_modules
import numpy as np

setup(
    name='broker',
    version='0.0.x',
    author='Brookhaven National Lab',
    packages=["broker",
              "broker.server",
              ],
    include_dirs=[np.get_include()],
    ext_modules=ext_modules
    )
