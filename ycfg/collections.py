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

# Standard imports
import abc
import collections
import functools
import pathlib
import yaml


class abstract_node_factory(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def node_type(self):
        pass

    @abc.abstractmethod
    def make_node(self):
        pass


class dict_node_factory(abstract_node_factory):

    @property
    def node_type(self):
        return dict

    def make_node(self):
        return dict()


class ordered_dict_node_factory(abstract_node_factory):

    @property
    def node_type(self):
        return collections.OrderedDict

    def make_node(self):
        return collections.OrderedDict()


class value_dict_pair(collections.UserDict):

    def __init__(self, value=None, data=dict()):
        self.data = data
        self.value = value


class dict_and_value_node_factory(abstract_node_factory):

    @property
    def node_type(self):
        return value_dict_pair

    def make_node(self):
        return value_dict_pair()


class folded_keys_dict(collections.UserDict):

    __no_streamline = True

    def __init__(self, data, node_factory=dict_node_factory(), __calling_protected_ctor__=None):
        self._dict_type = type(data)
        self.node_factory = node_factory
        if __calling_protected_ctor__ is not None and id(folded_keys_dict.__no_streamline) == id(__calling_protected_ctor__):
            self.data = data
        else:
            self.data = self._streamline_dict(data)


    #BEGIN Reduce functors
    def _build_node(self, state, item):
        if item not in state:
            state[item] = self.node_factory.make_node()

        return state[item]


    def _traverse_keys_path(self, data, key):
        if key in data:
            return data[key]

        raise KeyError('Oops')


    def _check_keys_path(self, state, key):
        if isinstance(state[0], self.node_factory.node_type):
            exists = key in state[0]
            return (state[0][key] if exists else None, exists)

        return tuple(None, False)
    #END Reduce functors


    def _streamline_dict(self, data):
        result = self._dict_type()

        for key, value in data.items():
            assert isinstance(key, str)                     # NOTE For other type of keys this container have no sense

            parts = key.split('.')

            if isinstance(value, self.node_factory.node_type):
                value = self._streamline_dict(value)

            functools.reduce(self._build_node, parts[:-1], result)[parts[-1]] =  value

        return result


    def __getitem__(self, key: str):
        assert isinstance(key, str)                         # NOTE For other type of keys this container have no sense

        parts = key.split('.')

        try:
            result = functools.reduce(self._traverse_keys_path, parts, self.data)

            if isinstance(result, self.node_factory.node_type):
                return folded_keys_dict(
                    result
                  , node_factory=self.node_factory
                  , __calling_protected_ctor__=folded_keys_dict.__no_streamline
                  )

            return result

        except KeyError:
            raise KeyError('Key not found: `{}`'.format(key))


    def __setitem__(self, key, value):
        parts = key.split('.')
        functools.reduce(self._build_node, parts[:-1], self.data)[parts[-1]] =  value


    def __delitem__(self, key):
        pass


    def __contains__(self, key):
        return functools.reduce(self._check_keys_path, key.split('.'), (self.data, True))[1]
