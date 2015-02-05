# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from future.builtins import str

from ent import Ent
from ent.json import loads, dumps


class TestEntJson(unittest.TestCase):

    def test_load_types(self):
        self.assertIsInstance(loads('1'), int)
        self.assertIsInstance(loads('1.0'), float)
        self.assertIsInstance(loads('true'), bool)
        self.assertIsInstance(loads('"foo"'), str)
        self.assertIsInstance(loads('[]'), list)
        self.assertIsInstance(loads('{}'), Ent)

        self.assertIs(loads('null'), None)

        self.assertRaises(ValueError, loads, 'foo')
        self.assertRaises(ValueError, loads, '{1,}')

    def test_dump_types(self):
        self.assertEqual(dumps(1), '1')
        self.assertEqual(dumps(1.0), '1.0')
        self.assertEqual(dumps(True), 'true')
        self.assertEqual(dumps(None), 'null')
        self.assertEqual(dumps([]), '[]')
        self.assertEqual(dumps({}), '{}')
        self.assertEqual(dumps(Ent()), '{}')
