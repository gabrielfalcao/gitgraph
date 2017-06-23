GitGraph - A git-backed graph database
======================================

This is an experimental project with idea taken from the `hexastore
<http://www.vldb.org/pvldb/1/1453965.pdf>`_ paper.

Usage:
------

.. code:: python

    from gitgraph import GitGraph
    from gitgraph import Subject

    store = GitGraph('my-git-cms')

    class Document(Subject):
        indexes = {'title'}
        fields = (
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

    uuid1 = 'deadbeefdeadbeefdeadbeefdeadbeef'
    uuid2 = '1c3b00da1c3b00da1c3b00da1c3b00da'

    # Subject can be created
    docs1 = store.create(
        'Document',
        uuid=uuid1,
        title='Essay',
        body='body1',
    )
    docs2 = store.create(
        Document,
        uuid=uuid2,
        title='Blog',
        body='body2',
    )

    store.commit()
    store.delete(docs1)
    store.commit()
    store.merge(docs1, docs2)
    docs1 = store.create(
        'Document',
        uuid=uuid1,
        title='Essay',
        body='body1',
    )
    docs2 = store.create(
        'Document',
        uuid=uuid2,
        title='Blog',
        body='body2',
    )
    store.commit()

    docs11 = store.get_subject_by_uuid('Document', uuid1)
    docs22 = store.get_subject_by_uuid(Document, uuid2)
    assert docs1 == docs11
    assert docs2 == docs22

    blog_documents = set(store.match_subjects_by_index('Document', 'title', lambda title: 'Blog' in title))
    assert len(blog_documents) == 2
    assert docs1 in blog_documents
    assert docs2 in blog_documents
    assert docs11 in blog_documents
    assert docs22 in blog_documents

    assert not set(store.scan_all('Document')).difference({blog1, blog2}}
    assert not set(store.scan_all(Document)).difference({blog11, blog22}}
    store.delete(docs2)
    store.commit()

    assert not set(store.scan_all(Document)).difference({blog1}}
    assert not set(store.scan_all('Document')).difference({blog1}}
    assert store.get_subject_by_uuid('Document', uuid1)
    assert not store.get_subject_by_uuid('Document', uuid2)



Basic Axioms:
-------------

- Every *subject name* is a root tree in the repository.
- Every *object* is stored as a git blob, but has a unique uuid which can be accessed through a special index.
- Every *indexed* **predicate** is a sub-tree containing blobs whose name in the tree is the blob_id of the original object, its value is the indexed value itself.
- Objects are stored in the tree under the path: ``SubjectName/objects/:blob_id``
- The blob-id of an **Object** can be retrieved at ``SubjectName/_ids/:uuid4``
- The *uuid4* of an **Object** can be retrieved at ``SubjectName/_uuids/:blob_id``
- Indexed predicates are stored in the tree with the path: ``SubjectName/indexes/<index name>/:blob_id``

Supported Operations
--------------------

- Create/Merge subjects by ``uuid4``
- Retrieve subjects by ``uuid4``
- Retrieve subjects by ``blob_id``
- Retrieve subjects by *indexed predicates*
- Delete nodes with all their references


TODO:
-----

- Support directed relationships
- Support querying by relationships
- Support GraphQL *(graphene-python ?)*
- Concurrent ZeroMQ server request/reply
- Replication through git-push
- Merge strategies *(git flow?)*
- Use git-hooks for real time notifications
