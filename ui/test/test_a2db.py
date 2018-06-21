import os
import logging
import unittest

import a2db
import uuid


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

temp_db_path = os.path.join(os.environ.get('TEMP'), str(uuid.uuid4()))
log.debug('temp_db: %s' % temp_db_path)
db = a2db.A2db(temp_db_path)


class Test(unittest.TestCase):

    def test1_set_changes(self):
        key = 'test_entry'
        table = 'test_table'
        # set to something different than default:
        defaults = {'some': str(uuid.uuid4()), 'value': 123}
        changes = {'value': 124}
        db.set_changes(key, changes, defaults, table)
        now = db.get(key, table)
        self.assertFalse(now['value'] == defaults['value'])

        # change to default
        changes['value'] = 123
        db.set_changes(key, changes, defaults, table)
        now = db.get(key, table)
        self.assertTrue(now is None)
        self.assertTrue(key not in db.keys(table))

        # set something that's not in defaults:
        changes = {'blaaaa': 'rabbits'}
        db.set_changes(key, changes, defaults, table)
        now = db.get(key, table)
        self.assertTrue(now == changes)
        db.pop(key, table)
        self.assertFalse(key in db.keys(table))
        db.drop_table(table)
        self.assertFalse(table in db.tables())

    def test2_get_changes(self):
        key = 'test_entry'
        table = 'test_table'

        # test nothing set at all
        defaults = {'some': str(uuid.uuid4()), 'value': 13374223}
        fetched = db.get_changes(key, defaults, table)
        self.assertEqual(defaults['some'], fetched['some'])
        self.assertEqual(defaults['value'], fetched['value'])

        # test set changes, get different and same
        changes = {'value': 8888, 'somethingelse': 'HFHWKEGFKKUSDK'}
        db.set_changes(key, changes, defaults, table)
        fetched = db.get_changes(key, defaults, table)
        self.assertEqual(defaults['some'], fetched['some'])
        self.assertNotEqual(defaults['value'], fetched['value'])
        db.pop(key, table)
        self.assertFalse(key in db.keys(table))
        db.drop_table(table)
        self.assertFalse(table in db.tables())

    def test4_shutdown(self):
        db.all()
        db._con.close()
        os.remove(temp_db_path)
        self.assertFalse(os.path.exists(temp_db_path))


if __name__ == "__main__":
    unittest.main()
