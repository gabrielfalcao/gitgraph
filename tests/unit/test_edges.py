# -*- coding: utf-8 -*-
#
# <Plural - Git-powered graph database library>
# Copyright (C) <2017>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from mock import MagicMock
from plural.models.edges import Edge
from plural.models.edges import resolve_edge_name
from plural.models.edges import resolve_edge
from plural.exceptions import EdgeDefinitionNotFound

from tests.edges import Car, Vehicle
from tests.unit.scenarios import BlobStub


def test_resolve_edge_name():
    'resolve_edge_name() should return a string'

    resolve_edge_name('Vehicle').should.equal('Vehicle')
    resolve_edge_name(None).should.equal('*')
    resolve_edge_name(Vehicle).should.equal('Vehicle')
    resolve_edge_name.when.called_with({}).should.have.raised(
        TypeError,
        'resolve_edge_name() takes a Edge subclass, a string or None. Got {}'
    )


def test_edge_resolve_definition_not_found():
    'Edge.definition() should raise exception if definition does not exist'

    Edge.definition.when.called_with('w00t?').should.have.raised(
        EdgeDefinitionNotFound,
        'there are no edge subclass defined with the name "w00t?"',
    )


def test_resolve_edge():
    'resolve_edge() should return a string'

    resolve_edge('Vehicle').should.equal(Vehicle)
    resolve_edge(Vehicle).should.equal(Vehicle)
    resolve_edge.when.called_with(None).should.have.raised(
        TypeError,
        'resolve_edge() takes a Edge subclass or a string. Got None'
    )


def test_subclasses_inherit_indexes():
    ('Edge subclasses should inherit indexes of its parent')

    Car.indexes.should.equal({
        'max_speed',
        'brand',
        'model',
    })


def test_get_related_blob_paths():
    ('Edge.get_related_blob_paths() should use its uuid to retrieve '
     'the path for all indexed fields and objects related to it')

    car = Car(uuid='deadbeef', name='Tesla', model='S')
    repository = MagicMock(name='repository')
    repository.__getitem__.side_effect = lambda oid: BlobStub(oid)
    repository.index.__getitem__.side_effect = lambda path: BlobStub(path)
    result = car.get_related_blob_paths(repository)
    result.should.equal([
        'Car/_ids/deadbeef',
        'Car/_uuids/4616f0d04cf8d19dbe59f14a8225487e40061ba8',
        'Car/indexes/uuid/4616f0d04cf8d19dbe59f14a8225487e40061ba8',
        'Car/objects/4616f0d04cf8d19dbe59f14a8225487e40061ba8',
        'Car/indexes/brand/4616f0d04cf8d19dbe59f14a8225487e40061ba8',
        'Car/indexes/max_speed/4616f0d04cf8d19dbe59f14a8225487e40061ba8',
        'Car/indexes/model/4616f0d04cf8d19dbe59f14a8225487e40061ba8',
    ])
