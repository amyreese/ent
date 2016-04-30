ent
===

.. image:: https://travis-ci.org/jreese/ent.svg?branch=master
    :target: https://travis-ci.org/jreese/ent


``ent`` is a basic framework for generating attribute-based data structures from
dictionary-like data sources::

    > from ent import Ent

    > obj = Ent(foo='foo', bar=None)

    > obj.foo
    u'foo'

    > obj.bar
    None

``ent`` can contain arbitrarily-nested hierarchies, as long as every node/leaf
is either a primitive type, or an ent::

    > obj = Ent({
        'foo': 'bar',
        'list': [1, 2, 3, 4],
        'inner': {
            'foo': 'baz',
            'bar': 'bang',
            },
        'ent': Ent(foo='bar'),
        })

    > obj.foo
    u'bar'

    > obj.list[2]
    3

    > obj.inner.foo
    u'baz'

``ent`` can be merged and diffed, and it will even enforce types when merging
keys that are shared::

    > ent1 = Ent(foo=1, bar=True)

    > ent2 = Ent(foo='hi', bar=False, goo='win')

    > Ent.merge(ent1, ent2)
    <Ent {'foo': 1, 'bar': False}>

    > Ent.diff(ent1, ent2)
    <Ent {'bar': False}>

``ent`` even provides a stand-in for the ``json`` and ``yaml`` modules to
automatically convert to and from Ent objects and raw JSON/YAML::

    > from ent import json, yaml

    > json.loads('{"foo": true, "bar": null}')
    <Ent {'foo': True, 'bar': None}>

    > json.dumps(Ent(foo=True, bar=None))
    u'{"foo": true, "bar": null}'

    > yaml.safe_load('bar: null\nfoo: true\n')
    <Ent {'foo': True, 'bar': None}>

    > yaml.dump(Ent(foo=True, bar=None))
    u'baz: 1\nfoo: bar\n'


why
---

When working with configs, or other content pulled from sources like JSON, it
can be really annoying to need to constantly use brackets to access nested
data structures.

Let's say we have a small JSON file containing my personal profile::

    {
        "name": "John Reese",
        "urls": {
            "blog": "https://noswap.com",
            "github": "https://github.com/jreese",
            "facebook": "https://www.facebook.com/nucleareclipse"
        }
    }

Now let's read in that data and print some of it out using the standard
``json`` module::

    import json

    with open(...) as f:
        data = json.load(f)

    name = data['name']
    url = data['urls']['github']

We can do better with ``ent``::

    from ent import json

    with open(...) as f:
        data = json.load(f)

    name = data.name
    url = data.urls.github


install
-------

ent is compatible with Python 2.7+ and Python 3.3+.
You can install it from PyPI with the following command::

    $ pip install ent


license
-------

ent is copyright 2015 John Reese, and is licensed under the MIT license.
