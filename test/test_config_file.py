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

''' Unit tests for config_file class '''

# Project specific imports
from context import make_data_filename
from ycfg.config_file import config, items_as_attributes

# Standard imports
import pytest


class config_file_tester:

    def empty_test(self):
        c = config(make_data_filename('empty.yaml'))

        assert len(c) == 0


    def not_a_dict_file_test(self):
        with pytest.raises(ValueError) as ex:
            c = config(make_data_filename('not-a-dict.yaml'))

        assert 'Config file expected to be a YAML dictionary, but it does not: `' in str(ex)


    def ordering_test(self, capfd, expected_out):
        c = config(make_data_filename('ordering-test.yaml'))

        assert c['zero'] == 0
        assert c['uno'] == 1

        print(c)

        stdout, stderr = capfd.readouterr()

        assert expected_out == stdout


class tricky_dict_tester:

    def empty_dict_test(self):
        d = items_as_attributes()
        with pytest.raises(AttributeError) as ex:
            print(d.some)


    def level_one_test(self):
        data = {}
        data['one'] = 1
        data['two'] = 2
        data['tree'] = 3

        d = items_as_attributes(data)
        assert d.one == 1
        assert d.two == 2
        assert d.tree == 3


    def level_two_test(self):
        data = {}
        data['english'] = {}
        data['english']['one'] = 1
        data['english']['two'] = 2
        data['english']['tree'] = 3
        data['bahasa'] = {}
        data['bahasa']['satu'] = 1
        data['bahasa']['dua'] = 2
        data['bahasa']['tiga'] = 3

        d = items_as_attributes(data)

        assert d.english.one == 1
        assert d.english.two == 2
        assert d.english.tree == 3

        assert d.bahasa.satu == 1
        assert d.bahasa.dua == 2
        assert d.bahasa.tiga == 3
