.. _Tutorial:


.. highlight:: bash



Basic Usage
===========

Instalation
-----------

.. code:: bash

    pip install plural


Declaring Edges
------------------


.. code:: python

    from plural import Plural
    from plural import Edge

    store = Plural('my-git-cms')

    class Document(Edge):
        indexes = {'title'}
        predicates = (
            ('title', codec.Unicode),
            ('body', codec.Unicode),
            ('created_at', codec.DateTime),
            ('published_at', codec.DateTime),
        )

        incoming = {
            'authored_by': Author,
        }
        outgoing = {
            'contains': Tag,
        }

Create
------

.. code:: python

    uuid1 = 'deadbeefdeadbeefdeadbeefdeadbeef'

    # providing your own uuid
    docs1 = store.create_edge(
        'Document',
        uuid=uuid1,
        title='Essay',
        body='body1',
    )

    # auto-generated uuid
    docs2 = store.create_edge(
        Document,
        title='Blog',
        body='body2',
    )

    store.commit()

    uuid2 = docs2.uuid


Querying
--------

One By UUID
~~~~~~~~~~~

.. code:: python

    # Using the class Document as edge type
    docs1 = store.get_edge_by_uuid(Document, uuid1)

    # Using the edge label
    docs2 = store.get_edge_by_uuid('Document', uuid2)


Many By Indexed Predicate
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python


    from plural.query import predicate
    # functional
    query = lambda title: 'Blog' in title

    # DSL
    query = predicate('title').contains('Blog')
    blog_documents = set(store.match_edges_by_index(Document, 'title', query))

    # With Regex
    query = predicate('title').matches('([Bb]log|[Ee]ssa[yi]s?)')
    blogs_and_essays = set(store.match_edges_by_index(Document, 'title', query))

Update
------

.. code:: python

    docs1.title = 'new title'

    docs2.title = 'documento dois'
    docs2.body = '<p>Hello</p>'

    store.merge(docs1, docs2)

    # recreate the doc1
    docs1 = store.create_edge(
        Document,
        uuid=uuid1,
        title='Essay',
        body='body1',
    )



Delete
------

.. code:: python

    store.delete(docs1)
    store.commit()

or

.. code:: python

    store.delete(docs1, auto_commit=True)
    store.commit()
