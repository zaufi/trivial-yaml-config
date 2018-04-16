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
    def assign_value(self, node, key, value):
        pass


    def make_node(self):
        return self.node_type()


class dict_node_factory(abstract_node_factory):

    @property
    def node_type(self):
        return dict

    def assign_value(self, node, key, value):
        node[key] = value


class ordered_dict_node_factory(abstract_node_factory):

    @property
    def node_type(self):
        return collections.OrderedDict


    def assign_value(self, node, key, value):
        node[key] = value


class value_dict_pair(collections.Mapping):

    def __init__(self, value=None, data=None):
        self.data = data if data is not None else {}
        self.value = value


    def __len__(self):
        return len(self.data)


    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]

        if hasattr(self.data.__class__, '__missing__'):
            return self.data.__class__.__missing__(self, key)

        raise KeyError(key)


    def __setitem__(self, key, value):
        self.data[key] = value


    def __delitem__(self, key):
        del self.data[key]


    def __iter__(self):
        return iter(self.data)


    def __contains__(self, key):
        return key in self.data


    def __eq__(self, other):
        if isinstance(other, type(self.data)):
            return self.data == other.data

        return self.value == other


    def __str__(self):
        return '({}, {})'.format(str(self.value), str(self.data))


    def __repr__(self):
        return '({}, {})'.format(repr(self.value), repr(self.data))


    def items(self):
        return self.data.items()


    def keys(self):
        return self.data.keys()


    def values(self):
        return self.data.values()


class dict_and_value_node_factory(abstract_node_factory):

    def __init__(self, node_prototype=None):
        self._prototype = node_prototype if node_prototype is not None else value_dict_pair()


    @property
    def node_type(self):
        return type(self._prototype)


    def make_node(self):
        type_ = type(self._prototype.data)
        return self.node_type(data=type_())


    def assign_value(self, node, key, value):
        if isinstance(value, self.node_type):
            node[key] = value
        else:
            if key not in node.data:
                node[key] = self.node_type()
            node[key].value = value


class folded_keys_dict(collections.Mapping):

    __no_straighten = True

    def __init__(self, data=None, node_factory=None, __calling_protected_ctor__=None):
        self.node_factory = node_factory if node_factory is not None else dict_node_factory()
        if data is None:
            data = {}
        if __calling_protected_ctor__ is not None and id(folded_keys_dict.__no_straighten) == id(__calling_protected_ctor__):
            self.data = data
        else:
            self.data = self._straighten_dict(data)


    #BEGIN Reduce functors
    def _build_node(self, state, item):
        '''
            TODO Make sure, if the node exists, it has a proper type
                 and we r not going to override anything...
        '''
        if item not in state:
            self.node_factory.assign_value(
                state
              , item
              , self.node_factory.make_node()
              )
        return state[item]


    def _traverse_keys_path(self, data, key):
        if isinstance(data, self.node_factory.node_type):
            return data[key]                                # NOTE May throw KeyError, and that is OK

        raise TypeError(key)


    def _check_keys_path(self, state, key):
        if isinstance(state[0], self.node_factory.node_type):
            exists = key in state[0]
            return (state[0][key] if exists else None, exists)

        return (None, False)
    #END Reduce functors


    def _straighten_dict(self, data):
        result = self.node_factory.make_node()

        for key, value in data.items():
            assert isinstance(key, str)                     # NOTE For other type of keys this container have no sense

            parts = key.split('.')

            if isinstance(value, self.node_factory.node_type):
                value = self._straighten_dict(value)

            self.node_factory.assign_value(
                functools.reduce(self._build_node, parts[:-1], result)
              , parts[-1]
              , value
              )

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
                  , __calling_protected_ctor__=folded_keys_dict.__no_straighten
                  )

            return result

        except KeyError:
            raise KeyError('Key not found: `{}`'.format(key))

        except TypeError as ex:
            raise TypeError('Key not indexable: `{}`'.format(str(ex)))


    def __setitem__(self, key, value):
        assert isinstance(key, str)                         # NOTE For other type of keys this container have no sense

        parts = key.split('.')
        self.node_factory.assign_value(
            functools.reduce(self._build_node, parts[:-1], self.data)
          , parts[-1]
          , value
          )


    def __delitem__(self, key: str):
        assert isinstance(key, str)                         # NOTE For other type of keys this container have no sense

        parts = key.split('.')

        node = functools.reduce(self._traverse_keys_path, parts[:-1], self.data)
        assert isinstance(node, self.node_factory.node_type)
        del node[parts[-1]]                                 # NOTE This may throw KeyError


    def __contains__(self, key: str):
        assert isinstance(key, str)                         # NOTE For other type of keys this container have no sense

        return functools.reduce(self._check_keys_path, key.split('.'), (self.data, True))[1]


    def __len__(self):
        return len(self.data)


    def __iter__(self):
        return iter(self.data)


    def items(self):
        return self.data.items()


    def keys(self):
        return self.data.keys()


    def values(self):
        return self.data.values()


    def update(self, other):
        return self.data.update(other.data)


    def __getattr__(self, key):
        '''
            See also `ItemsAsAttributes <https://github.com/jaraco/jaraco.collections/blob/master/jaraco/collections.py#L429>`_
        '''
        try:
            return getattr(super(folded_keys_dict, self), key)

        except AttributeError as ex:
            try:
                return getattr(self.data, key)
            except AttributeError:
                pass

            noval = object()

            def _safe_getitem(cont, key, missing_result):
                try:
                    return cont[key]

                except KeyError:
                    return missing_result

            result = _safe_getitem(self, key, noval)
            if result is not noval:
                return result

            message, = ex.args
            message = message.replace('super', self.__class__.__name__, 1)
            ex.args = message,
            raise


    def __str__(self):
        return str(self.data)


    def __repr__(self):
        return repr(self.data)


    def __eq__(self, other):
        return self.data == other.data if isinstance(other, folded_keys_dict) else other


class dict_stack(collections.Mapping):

    def __init__(self, *args, writable_layer=None):
        assert functools.reduce(lambda s, x: s and issubclass(type(x), collections.Mapping), args, True)
        self._stack = list(args)
        self._stack.reverse()
        self._writable_layer = writable_layer if writable_layer is not None else {}


    def keys(self):
        return list(set(itertools.chain.from_iterable(c.keys() for c in self)))


    def __getitem__(self, key):
        merged = None
        for scope in [self._writable_layer] + self._stack:
            # Is key exists at the current level
            if key in scope:
                # Yep, get it.
                item = scope[key]
                # If the key is partial, so `item` is a "subtree"
                if isinstance(item, folded_keys_dict):
                    # Yep, check if this is the first occurence...
                    if merged is None:
                        merged = item                       # ... then just assign it to future result.
                    else:
                        merged.update(item)                 # ... no, some results was found on previous levels, then merge!

                # Ok, item is just a value. Check if prevous levels gave no partial results.
                elif merged is None:
                    return scope[key]                       # No! Then just return found item.

                else:
                    raise ValueError()

        if merged is None:
            raise KeyError(key)

        # TODO Turn `merged` into read-only
        return merged


    def __setitem__(self, key, value):
        self._writable_layer[key] = value


    def __len__(self):
        return len(self._stack)


    def __iter__(self):
        return itertools.chain.from_iterable([self._writable_layer] + self._stack)
