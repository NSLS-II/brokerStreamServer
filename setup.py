#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(
    name='broker',
    version='0.0.x',
    author='Brookhaven National Lab',
    packages=["broker",
              "broker.server",
              'client'
              ],
    )
