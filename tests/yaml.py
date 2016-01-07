# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from past.builtins import basestring

from ent import Ent
from ent.yaml import safe_load, dump


class TestEntYaml(unittest.TestCase):

    def test_load_types(self):
        self.assertIsInstance(safe_load('1'), int)
        self.assertIsInstance(safe_load('1.0'), float)
        self.assertIsInstance(safe_load('true'), bool)
        self.assertIsInstance(safe_load('"foo"'), basestring)
        self.assertIsInstance(safe_load('[]'), list)
        self.assertIsInstance(safe_load('{}'), Ent)

        self.assertIs(safe_load('null'), None)

    def test_dump_types(self):
        self.assertEqual(dump(1), '1\n...\n')
        self.assertEqual(dump(1.0), '1.0\n...\n')
        self.assertEqual(dump(True), 'true\n...\n')
        self.assertEqual(dump(None), 'null\n...\n')
        self.assertEqual(dump([]), '[]\n')
        self.assertEqual(dump({}), '{}\n')
        self.assertEqual(dump(Ent()), '{}\n')
