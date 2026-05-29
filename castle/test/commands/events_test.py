from castle.test import unittest
from castle.command import Command
from castle.commands.events.schema import CommandsEventsSchema
from castle.commands.events.query import CommandsEventsQuery
from castle.commands.events.group import CommandsEventsGroup
from castle.errors import InvalidParametersError


class CommandsEventsTestCase(unittest.TestCase):
    def test_schema(self):
        self.assertEqual(
            CommandsEventsSchema.call(),
            Command(method='get', path='events/schema', data=None),
        )

    def test_query(self):
        options = {
            'filters': [{'field': 'name', 'op': '$eq', 'value': 'x'}],
            'sort': {'field': 'created_at', 'order': 'desc'},
        }
        self.assertEqual(
            CommandsEventsQuery.call(options),
            Command(method='post', path='events/query', data=options),
        )

    def test_query_invalid_filter(self):
        with self.assertRaises(InvalidParametersError):
            CommandsEventsQuery.call({'filters': [{'field': 'name'}]})

    def test_group(self):
        options = {'filters': [{'field': 'name', 'op': '$eq', 'value': 'x'}]}
        self.assertEqual(
            CommandsEventsGroup.call(options),
            Command(method='post', path='events/group', data=options),
        )

    def test_group_invalid_sort(self):
        with self.assertRaises(InvalidParametersError):
            CommandsEventsGroup.call({'sort': {'field': 'created_at'}})
