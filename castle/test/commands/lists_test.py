from castle.test import unittest
from castle.command import Command
from castle.commands.lists.create import CommandsListsCreate
from castle.commands.lists.get_all import CommandsListsGetAll
from castle.commands.lists.get import CommandsListsGet
from castle.commands.lists.query import CommandsListsQuery
from castle.commands.lists.update import CommandsListsUpdate
from castle.commands.lists.delete import CommandsListsDelete
from castle.errors import InvalidParametersError


class CommandsListsTestCase(unittest.TestCase):
    def test_create(self):
        options = {'name': 'my-list', 'color': '$grey', 'primary_field': 'user.email'}
        self.assertEqual(
            CommandsListsCreate.call(options), Command(method='post', path='lists', data=options)
        )

    def test_create_missing_required(self):
        with self.assertRaises(InvalidParametersError):
            CommandsListsCreate.call({'name': 'my-list'})

    def test_get_all(self):
        self.assertEqual(CommandsListsGetAll.call(), Command(method='get', path='lists', data=None))

    def test_get(self):
        self.assertEqual(
            CommandsListsGet.call({'list_id': 'abc'}),
            Command(method='get', path='lists/abc', data=None),
        )

    def test_get_missing_list_id(self):
        with self.assertRaises(InvalidParametersError):
            CommandsListsGet.call({})

    def test_query(self):
        options = {
            'filters': [{'field': 'name', 'op': '$eq', 'value': 'x'}],
            'sort': {'field': 'created_at', 'order': 'desc'},
        }
        self.assertEqual(
            CommandsListsQuery.call(options),
            Command(method='post', path='lists/query', data=options),
        )

    def test_query_invalid_filter(self):
        with self.assertRaises(InvalidParametersError):
            CommandsListsQuery.call({'filters': [{'field': 'name'}]})

    def test_update(self):
        self.assertEqual(
            CommandsListsUpdate.call({'list_id': 'abc', 'name': 'new'}),
            Command(method='put', path='lists/abc', data={'name': 'new'}),
        )

    def test_delete(self):
        self.assertEqual(
            CommandsListsDelete.call({'list_id': 'abc'}),
            Command(method='delete', path='lists/abc', data=None),
        )
