# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Alex Turbov <i.zaufi@gmail.com>
#
# Trivial YAML Config is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Trivial YAML Config is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

''' Helper functions for tests '''

# Standard imports
import contextlib
import os
import pathlib
import sys


# NOTE DO NOT REMOVE
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_data_dir = pathlib.Path(__file__).parent / 'data'


def data_dir():
    return _data_dir


def output_dir():
    return data_dir() / 'output'


def expected_results_dir():
    return data_dir() / 'expected-results'


def make_data_filename(filename):
    return data_dir() / filename


@contextlib.contextmanager
def change_work_dir(directory):
    assert isinstance(directory, pathlib.Path)
    assert directory.is_dir()

    save_current = pathlib.Path.cwd()
    os.chdir(str(directory))

    try:
        yield

    finally:
        os.chdir(str(save_current))
