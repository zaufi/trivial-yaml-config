# -*- coding: utf-8 -*-
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

# Standard imports
import collections
import yaml
import yaml.constructor


class ordered_dict_loader(yaml.Loader):
    '''
        A YAML loader that loads mappings into ordered dictionaries.

        See also: https://gist.github.com/enaeseth/844388
    '''

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)


    def construct_yaml_map(self, node):
        data = collections.OrderedDict()

        yield data

        value = self.construct_mapping(node)
        data.update(value)


    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None
              , None
              , 'expected a mapping node, but found {}'.format(node.id)
              , node.start_mark
              )

        mapping = collections.OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)

            except TypeError as ex:
                raise yaml.constructor.ConstructorError(
                    'while constructing a mapping'
                  , node.start_mark
                  , 'found unacceptable key `{}`'.format(ex)
                  , key_node.start_mark
                  )

            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping
