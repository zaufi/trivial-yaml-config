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

# Project specific imports
from .yaml import ordered_dict_loader

# Standard imports
import collections
import pathlib
import yaml


class items_as_attributes(collections.UserDict):

    def __init__(self, data={}):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            item = self.data[name]

            # Check if the item is a dict itself
            # TODO What about other type of dictionaries?
            if isinstance(item, type(self.data)):
                return items_as_attributes(item)

            # Ordinal item
            return item

        raise AttributeError('Key {} not found'.format(name))


class config(collections.UserDict):

    def __init__(self, filename: pathlib.Path):
        with filename.open('r') as f:
            data = yaml.load(f, ordered_dict_loader)

        if data is None:
            self.data = {}

        elif not isinstance(data, collections.OrderedDict):
            raise ValueError('Config file expected to be a YAML dictionary, but it does not: `{}`'.format(filename))

        else:
            self.data = data
