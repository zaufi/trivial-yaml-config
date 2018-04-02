#!/usr/bin/env python
#
# Copyright (c) 2017 Alex Turbov <i.zaufi@gmail.com>
#

# Project specific imports

# Standard imports
import pathlib
from setuptools import setup, find_packages
from ycfg.version import __version__

def sources_dir():
    return pathlib.Path(__file__).parent


def readfile(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.read()


def get_requirements_from(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.readlines()

setup(
    name             = 'ycfg'
  , version          = __version__
  , description      = 'Easy way to get and access configuration data from YAML files'
  , long_description = readfile('README.rst')
  , author           = 'Alex Turbov'
  , author_email     = 'I.zaufi@gmail.com'
  , url              = 'https://github.com/zaufi/trivial-yaml-config'
  , download_url     = 'https://github.com/zaufi/trivial-yaml-config/archive/release/{}.tar.gz'.format(__version__)
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
