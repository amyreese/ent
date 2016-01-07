# Copyright 2016 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import yaml

from ent import Ent


# mirror the basic yaml api
def dump(ent, *args, **kwargs):
    new_kwargs = {
        'default_flow_style': False,
    }
    new_kwargs.update(kwargs)

    try:
        obj = ent._encode()
    except:
        obj = ent

    return yaml.dump(obj, *args, **new_kwargs)


def safe_load(*args, **kwargs):
    obj = yaml.safe_load(*args, **kwargs)
    return Ent.load(obj)
