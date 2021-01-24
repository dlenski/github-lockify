#!/usr/bin/env python3

import sys, os
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

if not sys.version_info[0] == 3:
    sys.exit("Python 2.x is not supported; Python 3.x is required.")

########################################

setup(name="github-lockify",
      version=0.1,
      description="Lock closed GitHub issues en masse",
      long_description=open("description.rst").read(),
      author="Daniel Lenski",
      author_email="dlenski@gmail.com",
      license='GPL v3 or later',
      install_requires=[ 'requests>=2.0.0' ],
      url="https://github.com/dlenski/github-lockify",
      py_modules = ['github_lockify'],
      entry_points={ 'console_scripts': [ 'github-lockify=github_lockify:main' ] },
      extras_require={
        'hub': [ 'PyYAML>=3.0' ],
      }
      )
