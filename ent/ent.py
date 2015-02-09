# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future.builtins import bytes, str

SAFE_TYPES = (bool, int, float, bytes, str, tuple, list, dict, set)


class Singleton(type):
    """Metaclass for creating singleton objects.
    Requires the class to derive from object.

    Example:

        class Something(object):
            __metaclass__ = Singleton

        # create brand-new Something
        s1 = Something()

        # create a second Something
        s2 = Something()

        # compare the two instances
        assert id(s1) == id(s2)

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        obj = Singleton._instances.get(cls, None)

        if obj is None:
            obj = cls.__new__(cls)
            obj.__init__(*args, **kwargs)
            Singleton._instances[cls] = obj

        return obj


class Ent(object):
    """A basic object type that, given a dictionary or keyword arguments,
    converts the key/value pairs into object attributes."""

    def __init__(self, data=None, **kwargs):
        if data is None:
            data = {}
        data.update(kwargs)

        for key, value in list(data.items()):
            t = type(value)

            # prevent overwriting values with unsafe callables
            if (key in self.__class__.__dict__ and
                    t not in SAFE_TYPES):
                data.pop(key)

            if t in (tuple, list, set):
                value = Ent.load(value)
                data[key] = value

            elif t == dict:
                value = Ent(value)
                data[key] = value

        self.__dict__.update(data)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.__dict__)

    def _encode(self):
        """Generate a recursive JSON representation of the ent."""
        obj = {k: v for k, v in self.__dict__.items()
               if not k.startswith('_') and type(v) in SAFE_TYPES}
        obj.update({k: v._encode() for k, v in self.__dict__.items()
                   if isinstance(v, Ent)})
        return obj

    def copy(self):
        """Generate a new ent with the same keys and values."""
        return self.__class__.load(self)

    @classmethod
    def load(cls, data):
        """Create a new ent from an existing value.  The value must either
        be an instance of Ent, or must be an instance of SAFE_TYPES.  If
        the value is a base type (bool, int, string, etc), it will just be
        returned.  Iterable types will be loaded recursively, transforming
        dictionaries into Ent instances, but otherwise maintaining the
        hierarchy of the input data."""
        t = type(data)

        if t == cls:
            return cls({k: cls.load(v) for k, v in data.__dict__.items()})

        elif isinstance(data, Ent):
            return data.copy()

        elif t not in SAFE_TYPES:
            return None

        elif t in (tuple, list, set):
            return t(cls.load(i) for i in data)

        elif t == dict:
            return cls({k: cls.load(v) for k, v in data.items()})

        else:
            return data

    @classmethod
    def merge(cls, *args, **kwargs):
        """Create a new Ent from one or more existing Ents.  Keys in the
        later Ent objects will overwrite the keys of the previous Ents.
        Later keys of different type than in earlier Ents will be bravely
        ignored.

        The following keyword arguments are recognized:

        newkeys: boolean value to determine whether keys from later Ents
        should be included if they do not exist in earlier Ents.

        ignore: list of strings of key names that should not be overridden by
        later Ent keys.

        """
        newkeys = bool(kwargs.get('newkeys', False))
        ignore = kwargs.get('ignore', list())

        if len(args) < 1:
            raise ValueError('no ents given to Ent.merge()')
        elif not all(isinstance(s, Ent) for s in args):
            raise ValueError('all positional arguments to Ent.merge() must '
                             'be instances of Ent')

        ent = args[0]
        data = cls.load(ent)

        for ent in args[1:]:
            for key, value in ent.__dict__.items():
                if key in ignore:
                    continue

                if key in data.__dict__:
                    v1 = data.__dict__[key]
                    if type(value) == type(v1):
                        if isinstance(v1, Ent):
                            data.__dict__[key] = cls.merge(v1, value, **kwargs)
                        else:
                            data.__dict__[key] = cls.load(value)

                elif newkeys:
                    data.__dict__[key] = value

        return data

    @classmethod
    def diff(cls, *args, **kwargs):
        """Create a new Ent representing the differences in two or more
        existing Ents.  Keys in the later Ents with values that differ
        from the earlier Ents will be present in the final Ent with the
        latest value seen for that key.  Later keys of different type than in
        earlier Ents will be bravely ignored.

        The following keywoard arguments are recognized:

        newkeys: boolean value to determine whether keys from later Ents
        should be included if they do not exist in earlier Ents.

        ignore: list of strings of key names that will not be included.

        """
        newkeys = bool(kwargs.get('newkeys', False))
        ignore = kwargs.get('ignore', list())

        if len(args) < 2:
            raise ValueError('less than two ents given to Ent.diff()')
        elif not all(isinstance(s, Ent) for s in args):
            raise ValueError('all positional arguments to Ent.diff() must '
                             'be instances of Ent')

        s1 = args[0]
        differences = Ent()

        for s2 in args[1:]:
            for key, value in s2.__dict__.items():
                if key in ignore:
                    continue

                if key in s1.__dict__:
                    v1 = s1.__dict__[key]
                    if type(value) == type(v1):
                        if isinstance(v1, Ent):
                            delta = cls.diff(v1, value, **kwargs)
                            if len(delta.__dict__):
                                differences.__dict__[key] = delta
                        elif v1 != value:
                            differences.__dict__[key] = cls.load(value)

                elif newkeys:
                    differences.__dict__[key] = cls.load(value)

            s1 = s2

        return differences

    @classmethod
    def subclasses(cls):
        """Return a set of all Ent subclasses, recursively."""
        seen = set()
        queue = set([cls])

        while queue:
            c = queue.pop()
            seen.add(c)

            sc = c.__subclasses__()
            for c in sc:
                if c not in seen:
                    queue.add(c)

        seen.remove(cls)
        return seen
