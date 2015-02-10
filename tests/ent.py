# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from ent import Ent


class Foo(Ent):
    pass


class Bar(Foo):
    pass


class TestEnt(unittest.TestCase):

    def setUp(self):
        self.structure = {
            "scalar": 1,
            "list": [1, 2, 3, 4],
            "hash": {
                "scalar": 1,
                "list": [1, 2, 3, 4],
                "hash": {
                    "scalar": 1,
                }
            },
            "hashes": [
                {
                    "scalar": 1,
                    "list": [1, 2, 3, 4],
                    "hash": {
                        "scalar": 1,
                    }
                },
                {
                    "scalar": 1,
                    "list": [1, 2, 3, 4],
                    "hash": {
                        "scalar": 1,
                    }
                },
            ]
        }

    def test_attributes(self):
        ent = Ent.load(self.structure)

        self.assertEqual(ent.scalar, 1)

        self.assertIsInstance(ent.list, list)
        self.assertEqual(len(ent.list), 4)
        self.assertEqual(ent.list[2], 3)

        self.assertIsInstance(ent.hash, Ent)

        self.assertIsInstance(ent.hashes, list)
        self.assertEqual(len(ent.hashes), 2)
        self.assertIsInstance(ent.hashes[0], Ent)

    def test_nesting(self):
        ent = Ent.load(self.structure)

        self.assertEqual(ent.hash.scalar, 1)
        self.assertEqual(len(ent.hash.list), 4)
        self.assertEqual(ent.hash.list[2], 3)
        self.assertEqual(ent.hash.hash.scalar, 1)

        self.assertEqual(ent.hashes[0].scalar, 1)
        self.assertEqual(ent.hashes[0].list[1], 2)
        self.assertEqual(ent.hashes[1].hash.scalar, 1)

    def test_ent_subclasses(self):
        foo = Foo()
        bar = Bar()

        self.assertTrue(isinstance(foo, Ent))
        self.assertTrue(isinstance(foo, Foo))
        self.assertFalse(isinstance(foo, Bar))

        self.assertTrue(isinstance(bar, Ent))
        self.assertTrue(isinstance(bar, Foo))
        self.assertTrue(isinstance(bar, Bar))

        foo = Foo.load({'foo': 'bar'})

        self.assertTrue(isinstance(foo, Ent))
        self.assertTrue(isinstance(foo, Foo))
        self.assertFalse(isinstance(foo, Bar))

        bar = Bar.load({'foo': 'bar'})

        self.assertTrue(isinstance(bar, Ent))
        self.assertTrue(isinstance(bar, Foo))
        self.assertTrue(isinstance(bar, Bar))

    def test_constructor_vs_load(self):
        ent1 = Ent(self.structure)
        ent2 = Ent.load(self.structure)

        self.assertEqual(ent1.scalar, ent2.scalar)
        self.assertEqual(ent1.list, ent2.list)

        self.assertEqual(ent1.hash.scalar, ent2.hash.scalar)
        self.assertEqual(ent1.hash.list, ent2.hash.list)
        self.assertEqual(ent1.hash.hash.scalar, ent2.hash.hash.scalar)

        self.assertEqual(ent1.hashes[0].scalar, ent2.hashes[0].scalar)
        self.assertEqual(ent1.hashes[0].list, ent2.hashes[0].list)
        self.assertEqual(ent1.hashes[0].hash.scalar,
                         ent2.hashes[0].hash.scalar)

        self.assertEqual(ent1.hashes[1].scalar, ent2.hashes[1].scalar)
        self.assertEqual(ent1.hashes[1].list, ent2.hashes[1].list)
        self.assertEqual(ent1.hashes[1].hash.scalar,
                         ent2.hashes[1].hash.scalar)

    def test_foo_stays_foo(self):
        foo = Foo()

        ent = Ent(foo=foo)
        self.assertTrue(isinstance(ent.foo, Foo))

        ent = Ent(foos=[foo])
        self.assertTrue(isinstance(ent.foos[0], Foo))

        ent = Ent(hash={'foo': foo})
        self.assertTrue(isinstance(ent.hash.foo, Foo))

        ent = Ent.load(foo)
        self.assertTrue(isinstance(ent, Foo))

        ent = Ent.load([foo])
        self.assertTrue(isinstance(ent[0], Foo))

        ent = Ent.load({'foo': foo})
        self.assertTrue(isinstance(ent.foo, Foo))

    def test_foo_promotion(self):
        base = Ent()

        ent = Foo.load(base, promote=True)
        self.assertTrue(isinstance(ent, Foo))

        ent = Foo.load(base, promote=False)
        self.assertFalse(isinstance(ent, Foo))

        ent1 = Foo.load(base, promote=True)
        ent = Bar.load(ent1, promote=True)
        self.assertTrue(isinstance(ent, Bar))

        ent1 = Foo.load(base, promote=True)
        ent = Bar.load(ent1, promote=False)
        self.assertTrue(isinstance(ent, Foo))
        self.assertFalse(isinstance(ent, Bar))

        ent1 = Foo.load(base, promote=False)
        ent = Bar.load(ent1, promote=True)
        self.assertTrue(isinstance(ent, Bar))

        ent1 = Foo.load(base, promote=False)
        ent = Bar.load(ent1, promote=False)
        self.assertTrue(isinstance(ent, Ent))
        self.assertFalse(isinstance(ent, Foo))
        self.assertFalse(isinstance(ent, Bar))

    @unittest.expectedFailure
    def test_dict_access(self):
        ent = Ent.load(self.structure)

        self.assertEqual(len(ent.hash), 3)
        self.assertTrue('scalar' in ent.hash)
