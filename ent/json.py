# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json

from functools import partial

from ent import Ent


def object_hook(obj):
    return Ent.load(obj)


class EntEncoder(json.JSONEncoder):
    """A simple JSON encoder that looks for objects with a _encode() method,
    and uses that to return their JSON representation."""

    def default(self, o):
        try:
            return o._encode()
        except:
            return str(o)


class EntDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, object_hook=object_hook)


# mirror the json library
dump = partial(json.dump, cls=EntEncoder)
dumps = partial(json.dumps, cls=EntEncoder)
load = partial(json.load, object_hook=object_hook)
loads = partial(json.loads, object_hook=object_hook)
