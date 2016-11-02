"""
a2db - wrapper to the a2 database

Mainly we store key value pairs. So the 'tables' are more or less
id key  value
-------------
01 this 0.5
02 that 'lala'
03 blib 'something'
04 blob 'something'

lets see how we deal with 'real' tables in the future... if we need to

this enables us to do simple get/set things like

incls = a2db.get('includes', 'a2')
a2db.set('includes', 'a2', incls)
a2db.rem('tempstuff', 'a2')
"""
import json
import sqlite3
from copy import deepcopy

import a2core


log = a2core.get_logger(__name__)
_defaultTable = 'a2'
_defaultSep = '|'


class A2db(object):
    def __init__(self, a2dbFile):
        self._file = a2dbFile
        self._con = sqlite3.connect(a2dbFile)
        self._cur = self._con.cursor()
        log.info('initialised! (%s)' % self._file)

    def get(self, key, table=_defaultTable, check=True, asjson=True):
        """
        Gets you a value from a keyName and tableName.

        This correctly triggers the key error because fetch silently returns [] if key is not
        available. So return [0] fails! And not fetch. But ok thats good :]
        :param key: keyName in the "key" column
        :param table: tableName
        :param: check: will look for the key in table before even trying to fetch
        :param: asjson: Only for fixing legacy stuff with the db. Just gets the string from a field
        :return: string of the data or empty string
        """
        if check and table not in self.tables():
            return None

        if check and key not in self.keys(table):
            return None

        try:
            data = self._fetch('select value from "%s" where key="%s"' % (table, key))[0][0]
            if not asjson:
                return data
            return json.loads(data)
#             except:
#                 raise Exception('Failed converting data: %s' % data)

        except Exception as error:
            if table not in self.tables():
                log.error('there is no table named "%s"' % table)
                return None
            elif key not in self.keys(table):
                log.error('there is no key "%s" in section "%s"' % (key, table))
                return None
            else:
                log.error('Error getting data from key "%s" from table "%s"' % (key, table))
                raise error

    def set(self, key, value, table=_defaultTable):
        """
        update TableName SET valueName=value WHERE key=keyName
        """
        jvalue = json.dumps(value, separators=(',', ':'))
        jvalue = jvalue.replace('"', '""')
        try:
            if key not in self.keys(table):
                statement = ('insert into "%s" ("key","value") values ("%s", "%s")'
                             % (table, key, jvalue))
                log.debug('adding value!\n  %s' % statement)
            else:
                statement = 'update "%s" set value="%s" WHERE key="%s"' % (table, jvalue, key)
                log.debug('updating value!\n  %s' % statement)
            self._execute(statement)
            self._con.commit()
        # except sqlite3.DatabaseError as error:
        except Exception as error:
            # except:
            log.debug('setting db failed...')
            if table not in self.tables():
                log.debug('creating table and retry...')
                self.createTable(table)
                # TODO: resolve loop:
                self.set(key, value, table)
            else:
                log.error('could not set value: "%s" on key:"%s" in section:"%s"\n%s'
                          % (value, key, table, error))
                # log.error('could not set value: "%s" on key:"%s" in section:"%s"'
                #          % (value, key, table))

    def pop(self, key, table=_defaultTable):
        """
        removes a whole entry from a table. So the whole row: index, key and value will be gone
        """
        if key not in self.keys(table):
            return
        statement = ('delete from "%s" where key="%s"' % (table, key))
#         delete from where key
#             statement = 'delete "%s" set value="%s" WHERE key="%s"' % (table, value, key)
#             log.debug('updating value!\n  %s' % statement)
        self._execute(statement)
        self._con.commit()

    def tables(self):
        tablelist = self._fetch("SELECT name FROM sqlite_master WHERE type='table'")
        return [t[0] for t in tablelist]

    def dropTable(self, table):
        if table not in self.tables():
            return
        self._execute('drop table "%s"' % table)
        self._con.commit()

    def keys(self, table=_defaultTable):
        data = self._fetch('select key from "%s"' % table)
        return [k[0] for k in data]

    def _fetch(self, statement):
        self._execute(statement)
        return self._cur.fetchall()

    def createTable(self, table):
        if table in self.tables():
            return
        statement = 'create table "%s" (id integer primary key, key TEXT, value TEXT)' % table
        log.debug('createTable statement:\n\t%s' % statement)
        self._execute(statement)

    def _execute(self, statement):
        try:
            self._cur.execute(statement)
        except Exception as err:
            raise Exception('statement execution fail: "%s\nerror: %s' % (statement, err))
            # log.error('statement execution fail: "%s\nerror: %s' % (statement, err))

    def all(self):
        tables = self.tables()
        for t in tables:
            columns = ' - '.join([i[1] for i in self._fetch('PRAGMA table_info("%s")' % t)])
            log.info('\ntable: "%s":\n  %s\n  %s\n  %s'
                     % (t, columns, '-' * 40,
                        '\n  '.join([str(i)[1:-1] for i in self._fetch('select * from "%s"' % t)])))

    def set_changes(self, key, changes_dict, defaults_dict, table=_defaultTable):
        """
        Writes differences from defaults_dict to the db.

        To keep the data in db at a minumum. The key is deleted
        when there are no changes from the default_dict.
        """
        current = self.get(key, table) or {}
        changed = False
        for value_name, value in changes_dict.items():
            if value_name not in defaults_dict:
                log.info('Setting "%s:%s" to "%s|%s" Which is not in defaults_dict!'
                         % (value_name, str(value), table, key))

            if defaults_dict.get(value_name) != value:
                # value is not default
                if current.get(value_name) == value:
                    # value is already set! done!
                    continue
                else:
                    # else set it
                    current[value_name] = value
                    changed = True
            elif value_name in current:
                # value is default
                log.debug('value "%s" is default %s.. deleting...' % (value_name, value))
                del current[value_name]
                changed = True
        if changed:
            if current:
                self.set(key, current, table)
            else:
                self.pop(key, table)

    def get_changes(self, key, default_dict, table=_defaultTable):
        """
        Fetches settings from the db if set in the db and different from the
        given default_dict.
        """
        current = self.get(key, table) or {}
        result = deepcopy(default_dict)
        for value_name, value in default_dict.items():
            if value_name in current:
                set_value = current.get(value_name)
                if set_value != value:
                    result[value_name] = set_value
        return result


if __name__ == '__main__':
    import unittest
    import test.test_a2db
    print('test.test_a2db: %s' % test.test_a2db)
    unittest.main(test.test_a2db, verbosity=2)
