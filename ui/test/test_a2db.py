'''
ui.test.test_a2db
Created on 18.08.2016

@author: eric
'''
import os
import logging
import unittest
from os.path import abspath, join, exists

import a2db
import uuid


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

temp_db_path = join(os.environ.get('TEMP'), str(uuid.uuid4()))
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

    def test2_shutdown(self):
        db.all()
        db._con.close()
        os.remove(temp_db_path)
        self.assertFalse(exists(temp_db_path))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
