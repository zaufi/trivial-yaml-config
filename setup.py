#!/usr/bin/env python
#
# Copyright (c) 2017 Alex Turbov <i.zaufi@gmail.com>
#

# Project specific imports
# TODO Import package/module w/ `__version__` variable

# Standard imports
import pathlib
from setuptools import setup, find_packages


def sources_dir():
    return pathlib.Path(__file__).parent


def readfile(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.read()


def get_requirements_from(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.readlines()

# TODO Set proper version (or import your package with __version__ variable)
version = '0.1.0'

setup(
    name             = 'Skeleton.py'
  , version          = version
  , description      = ''
  , long_description = readfile('README.rst')
  , author           = 'Alex Turbov'
  , author_email     = 'I.zaufi@gmail.com'
  , url              = ''
  , download_url     = 'https://github.com/zaufi/{name}/archive/release/{version}.tar.gz'.format(name, version)
  , packages         = find_packages(exclude=('test'))
  , license          = 'GNU General Public License v3 or later (GPLv3+)'
  , classifiers      = [
        'Development Status :: 4 - Beta'
      , 'Intended Audience :: Developers'
      , 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
      , 'Natural Language :: English'
      , 'Programming Language :: Python :: 3'
      ]
  , keywords         = ''
  , install_requires = get_requirements_from('requirements.txt')
  , test_suite       = 'test'
  , tests_require    = get_requirements_from('test-requirements.txt')
  , zip_safe         = True
  )
