# encoding: utf-8
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

    def test1_get_set(self):
        table = 'test'

        val_int = 2342
        val_float = 1.337
        val_str = str(uuid.uuid4())
        val_list = list(val_str)
        val_dict = {'val_int': val_int,
                    'val_float': val_float,
                    'val_str': val_str,
                    'val_list': val_list}

        for key, value in val_dict.items():
            db.set(key, value, table)
            ret_value = db.get(key, table)
            self.assertEqual(ret_value, value)
            self.assertEqual(type(ret_value), type(value))

        string_test = ('Another String with \'\" so called "quotation marks",\n'
                       'a linebreak, emoji👍  and a key with spaces in it!.')
        db.set('string test', string_test, table)
        ret_value = db.get('string test', table)
        self.assertEqual(ret_value, string_test)

        db.set('val_dict', val_dict, table)
        ret_value = db.get('val_dict', table)
        self.assertEqual(ret_value, val_dict)

        db.drop_table(table)
        self.assertFalse(table in db.tables())

    def test2_set_changes(self):
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

    def test3_get_changes(self):
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
        db.log_all()
        db._con.close()
        os.remove(temp_db_path)
        self.assertFalse(os.path.exists(temp_db_path))

    def test_check(self):
        self.fail('implement check test')


if __name__ == "__main__":
    unittest.main()
