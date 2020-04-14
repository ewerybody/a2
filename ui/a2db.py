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
import os
import json
import sqlite3

import a2core

log = a2core.get_logger(__name__)
_DEFAULTTABLE = 'a2'


class A2db(object):
    def __init__(self, db_file_path=None):
        if not db_file_path:
            raise RuntimeError('Cannot create db without file path!')

        self._file = db_file_path
        self._con = None
        self._cur = None
        self._db_file_exists = False
        log.info('initialised! (%s)' % self._file)

    @property
    def db_file_exists(self):
        if self._db_file_exists:
            return True
        self._db_file_exists = os.path.isfile(self._file or '')
        return self._db_file_exists

    def _ensure_db_file_exists(self):
        if self.db_file_exists:
            return

        directory = os.path.dirname(self._file)
        os.makedirs(directory, exist_ok=True)
        with open(self._file, 'wb') as fobj:
            fobj.write(bytes())
        print('db file created: %s' % self._file)

    def connect(self):
        self._con = sqlite3.connect(self._file)
        self._cur = self._con.cursor()

    def disconnect(self):
        self._con.close()

    def get(self, key, table=_DEFAULTTABLE, check=True, asjson=True):
        """
        Gets you a value from a keyName and tableName.

        This correctly triggers the key error because fetch silently returns [] if key is not
        available. So return [0] fails! And not fetch. But ok thats good :]
        :param key: keyName in the "key" column
        :param table: tableName
        :param check: will look for the key in table before even trying to fetch
        :param asjson: Only for fixing legacy stuff with the db. Just gets the string from a field
        :return: string of the data or empty string
        """
        if not self.db_file_exists:
            return None

        if check and table not in self.tables():
            return None

        if check and key not in self.keys(table):
            return None

        try:
            statement = f'select value from "{table}" where key=?'
            data = self._fetch(statement, (key,))[0][0]
            if not asjson:
                return data
            try:
                result = json.loads(data)
            except json.JSONDecodeError:
                result = json.loads(data.replace('""', '"'))
            return result

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

    def set(self, key, value, table=_DEFAULTTABLE, _table_create_flag=False):
        """
        update TableName SET valueName=value WHERE key=keyName
        """
        self._ensure_db_file_exists()

        jvalue = json.dumps(value, separators=(',', ':'))
        try:
            if key not in self.keys(table):
                statement = f'insert into "{table}" (key, value) values (?, ?)'
                values = (key, jvalue)
                log.debug('adding value!\n  %s' % statement)
            else:
                statement = f'update "{table}" set value=? WHERE key=?'
                values = (jvalue, key)
                log.debug('updating value!\n  %s' % statement)
            self._commit(statement, values)

        except Exception as error:
            log.debug('setting db failed...')
            if table not in self.tables():
                if _table_create_flag:
                    raise RuntimeError('a2db table creation was already attempted, failed again!')
                else:
                    log.debug('creating table and retry...')
                    self._create_table(table)
                    self.set(key, value, table, _table_create_flag=True)
            else:
                log.error('could not set value: "%s" on key:"%s" in section:"%s"\n%s'
                          % (value, key, table, error))

    def pop(self, key, table=_DEFAULTTABLE):
        """
        removes a whole entry from a table. So the whole row: index, key and value will be gone
        """
        if not self.db_file_exists:
            return None

        if table not in self.tables():
            return None

        if key not in self.keys(table):
            return

        statement = f'delete from "{table}" where key=?'
        self._commit(statement, (key,))

    def tables(self):
        tablelist = self._fetch("SELECT name FROM sqlite_master WHERE type='table'")
        return [t[0] for t in tablelist]

    def drop_table(self, table):
        self._ensure_db_file_exists()
        if table not in self.tables():
            return
        self._commit(f'drop table "{table}"')

    def keys(self, table=_DEFAULTTABLE):
        statement = f'select key from "{table}"'
        data = self._fetch(statement)
        return [k[0] for k in data]

    def _fetch(self, statement, values=None):
        try:
            self.connect()

            if values is None:
                self._cur.execute(statement)
            else:
                self._cur.execute(statement, values)

            results = self._cur.fetchall()
            self.disconnect()

        except Exception as err:
            raise Exception('statement execution fail: "%s\nerror: %s' % (statement, err))

        return results

    def create_table(self, table):
        self._ensure_db_file_exists()
        if table in self.tables():
            return
        self._create_table(table)
        self._con.commit()
        self.disconnect()

    def _create_table(self, table):
        self.connect()
        statement = (f'create table "{table}" '
                     '(id integer primary key, key TEXT, value TEXT)')
        log.debug('create_table statement:\n\t%s' % statement)
        self._cur.execute(statement)

    def _commit(self, statement, values=None):
        try:
            self.connect()
            if values is None:
                self._cur.execute(statement)
            else:
                self._cur.execute(statement, values)
            self._con.commit()
            self.disconnect()
        except Exception as err:
            raise Exception('statement execution fail: "%s\nerror: %s' % (statement, err))

    def _execute(self, statement):
        try:
            self.connect()
            self._cur.execute(statement)
            self.disconnect()
        except Exception as err:
            raise Exception('statement execution fail: "%s\nerror: %s' % (statement, err))

    def all(self):
        log.info(self._get_digest())

    def _get_digest(self):
        tables = sorted(self.tables())
        header = ('\n\n{line}table "%s"\n'
                  '  id - key - value\n'
                  '{line}  ').format(line='-' * 40 + '\n')
        text = 'database dump from %s\n' % self._file
        text += '%i tables: %s' % (len(tables), ', '.join(tables))
        for t in tables:
            statement = f'select * from "{t}"'
            data = self._fetch(statement)
            text += header % t
            text += '\n  '.join([str(i)[1:-1] for i in data])
        return text

    def set_changes(self, key, changes_dict, defaults_dict, table=_DEFAULTTABLE):
        """
        Writes differences from defaults_dict to the db.

        To keep the data in db at a minimum the key is deleted
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

    def get_changes(self, key, default_dict, table=_DEFAULTTABLE):
        """
        Fetches settings from the db if set in the db and different from the
        given default_dict.
        """
        current = self.get(key, table) or {}
        result = default_dict.copy()
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
