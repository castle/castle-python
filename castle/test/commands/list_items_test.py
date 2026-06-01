from castle.test import unittest
from castle.command import Command
from castle.commands.list_items.create import CommandsListItemsCreate
from castle.commands.list_items.create_batch import CommandsListItemsCreateBatch
from castle.commands.list_items.get import CommandsListItemsGet
from castle.commands.list_items.query import CommandsListItemsQuery
from castle.commands.list_items.count import CommandsListItemsCount
from castle.commands.list_items.update import CommandsListItemsUpdate
from castle.commands.list_items.archive import CommandsListItemsArchive
from castle.commands.list_items.unarchive import CommandsListItemsUnarchive
from castle.errors import InvalidParametersError


class CommandsListItemsTestCase(unittest.TestCase):
    def test_create(self):
        options = {'list_id': 'abc', 'author': '$user', 'primary_value': 'a@b.com'}
        self.assertEqual(
            CommandsListItemsCreate.call(options),
            Command(
                method='post',
                path='lists/abc/items',
                data={'author': '$user', 'primary_value': 'a@b.com'},
            ),
        )

    def test_create_missing_required(self):
        with self.assertRaises(InvalidParametersError):
            CommandsListItemsCreate.call({'list_id': 'abc'})

    def test_create_batch(self):
        options = {'list_id': 'abc', 'items': [{'primary_value': 'a@b.com'}]}
        self.assertEqual(
            CommandsListItemsCreateBatch.call(options),
            Command(
                method='post',
                path='lists/abc/items/batch',
                data={'items': [{'primary_value': 'a@b.com'}]},
            ),
        )

    def test_get(self):
        self.assertEqual(
            CommandsListItemsGet.call({'list_id': 'abc', 'list_item_id': 'i1'}),
            Command(method='get', path='lists/abc/items/i1', data=None),
        )

    def test_query(self):
        options = {'list_id': 'abc', 'filters': [{'field': 'f', 'op': '$eq', 'value': 'v'}]}
        self.assertEqual(
            CommandsListItemsQuery.call(options),
            Command(
                method='post',
                path='lists/abc/items/query',
                data={'filters': [{'field': 'f', 'op': '$eq', 'value': 'v'}]},
            ),
        )

    def test_count(self):
        self.assertEqual(
            CommandsListItemsCount.call({'list_id': 'abc'}),
            Command(method='post', path='lists/abc/items/count', data={}),
        )

    def test_update(self):
        options = {'list_id': 'abc', 'list_item_id': 'i1', 'comment': 'note'}
        self.assertEqual(
            CommandsListItemsUpdate.call(options),
            Command(method='put', path='lists/abc/items/i1', data={'comment': 'note'}),
        )

    def test_update_missing_comment(self):
        with self.assertRaises(InvalidParametersError):
            CommandsListItemsUpdate.call({'list_id': 'abc', 'list_item_id': 'i1'})

    def test_archive(self):
        self.assertEqual(
            CommandsListItemsArchive.call({'list_id': 'abc', 'list_item_id': 'i1'}),
            Command(method='delete', path='lists/abc/items/i1/archive', data=None),
        )

    def test_unarchive(self):
        self.assertEqual(
            CommandsListItemsUnarchive.call({'list_id': 'abc', 'list_item_id': 'i1'}),
            Command(method='put', path='lists/abc/items/i1/unarchive', data=None),
        )
