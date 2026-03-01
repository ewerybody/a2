"""
a2db - wrapper to the a2 database

Mainly we store key value pairs. So the 'tables' are more or less
id key  value
-------------
01 this 0.5
02 that 'lala'
03 biib 'something'
04 blob 'something'

lets see how we deal with 'real' tables in the future... if we need to

this enables us to do simple get/set things like

includes = a2db.get('includes', 'a2')
a2db.set('includes', 'a2', includes)
a2db.pop('temp_stuff', 'a2')
"""

import os
import json
import sqlite3
from contextlib import contextmanager
from collections.abc import Iterator

import a2core

log = a2core.get_logger(__name__)
_DEFAULT_TABLE = a2core.NAME


class A2db:
    """A2 Database abstraction class."""

    def __init__(self, db_file_path: str):
        if not db_file_path:
            raise RuntimeError('Cannot create db without file path!')

        self._file: str = db_file_path
        self._con: sqlite3.Connection | None = None
        self._cur: sqlite3.Cursor | None = None
        self._db_file_exists: bool = False
        log.info('initialized! (%s)', self._file)

    def get(self, key, table=_DEFAULT_TABLE, check=True, as_json=True):
        """
        Get a value from a key (in a and table).

        This correctly triggers the key error because fetch silently returns [] if key is not
        available. So return [0] fails! And not fetch. But ok thats good :]
        :param key: keyName in the "key" column
        :param table: tableName
        :param check: will look for the key in table before even trying to fetch
        :param as_json: Only for fixing legacy stuff with the db. Just gets the string from a field
        :return: string of the data or empty string
        """
        if not self.db_file_exists:
            return None

        with self._connection():
            if check and table not in self.tables():
                return None

            if check and key not in self.keys(table):
                return None

            try:
                statement = f'select value from "{table}" where key=?'
                data = self._fetch(statement, (key,))[0][0]
                if as_json:
                    try:
                        result = json.loads(data)
                    except json.JSONDecodeError:
                        result = json.loads(data.replace('""', '"'))
                else:
                    result = data
                return result

            except Exception as error:
                if table not in self.tables():
                    log.error('there is no table named "%s"', table)
                    return None

                if key not in self.keys(table):
                    log.error('there is no key "%s" in section "%s"', key, table)
                    return None

                log.error(
                    'Error getting data from key "%s" from table "%s"', key, table
                )
                raise error

    def set(self, key, value, table=_DEFAULT_TABLE, _table_create_flag=False):
        """
        Set or update a key/value pair (in a table).
        """
        self._ensure_db_file_exists()

        j_value = json.dumps(value, separators=(',', ':'))
        with self._connection():
            try:
                if key not in self.keys(table):
                    statement = f'insert into "{table}" (key, value) values (?, ?)'
                    values = (key, j_value)
                    log.debug('adding value!\n  %s', statement)
                else:
                    statement = f'update "{table}" set value=? WHERE key=?'
                    values = (j_value, key)
                    log.debug('updating value!\n  %s', statement)
                self._commit(statement, values)

            except Exception as error:
                log.debug('setting db failed...')
                if table in self.tables():
                    msg = 'could not set value: "%s" on key:"%s" in section:"%s"\n%s'
                    log.error(msg, value, key, table, error)
                    return

                if _table_create_flag:
                    raise RuntimeError(
                        'a2db table creation was already attempted, failed again!'
                    )
                else:
                    log.debug('creating table and retry...')
                    self._create_table(table)
                    self.set(key, value, table, _table_create_flag=True)

    def pop(self, key, table=_DEFAULT_TABLE):
        """
        Removes a whole entry from a table. So the whole row: index, key and value will be gone.
        """
        if not self.db_file_exists:
            return
        with self._connection():
            if table not in self.tables():
                return

            if key not in self.keys(table):
                return

            statement = f'delete from "{table}" where key=?'
            self._commit(statement, (key,))

    def tables(self):
        """Give list of tables on the db."""
        table_list = self._fetch("SELECT name FROM sqlite_master WHERE type='table'")
        return [t[0] for t in table_list]

    def keys(self, table=_DEFAULT_TABLE):
        """Give list of keys in a table."""
        statement = f'select key from "{table}"'
        data = self._fetch(statement)
        return [k[0] for k in data]

    def create_table(self, table):
        """Make a new table if it not yet exists."""
        self._ensure_db_file_exists()
        with self._connection():
            if table in self.tables():
                return
            self._create_table(table)

    def drop_table(self, table):
        """Remove a table from the db."""
        if not self.db_file_exists:
            return
        self._ensure_db_file_exists()
        with self._connection():
            if table not in self.tables():
                return
            self._commit(f'drop table "{table}"')

    def set_changes(self, key, changes_dict, defaults_dict, table=_DEFAULT_TABLE):
        """
        Write differences from defaults_dict to the db.

        To keep the data in db at a minimum the key is deleted
        when there are no changes from the default_dict.
        """
        with self._connection():
            current = self.get(key, table) or {}
            changed = False
            for value_name, value in changes_dict.items():
                if value_name not in defaults_dict:
                    msg = 'Setting "%s|%s" to "%s:%s" Which is not in defaults_dict!'
                    log.info(msg, table, key, value_name, str(value))

                if defaults_dict.get(value_name) != value:
                    # value is not default
                    if current.get(value_name) == value:
                        # value is already set! done!
                        continue
                    # else set it
                    current[value_name] = value
                    changed = True
                elif value_name in current:
                    # value is default
                    log.debug(
                        'value "%s" is default (%s).. deleting...', value_name, value
                    )
                    del current[value_name]
                    changed = True
            if changed:
                if current:
                    self.set(key, current, table)
                else:
                    self.pop(key, table)

    def get_changes(self, key, default_dict, table=_DEFAULT_TABLE):
        """
        Fetch settings from the db if set in the db and different from the
        given default_dict.
        """
        from copy import deepcopy

        current = self.get(key, table) or {}
        result = deepcopy(default_dict)
        for value_name, value in default_dict.items():
            if value_name in current:
                set_value = current.get(value_name)
                if set_value != value:
                    result[value_name] = set_value
        return result

    def disconnect(self):
        """Disconnect from the sqlite db.
        You should not need to use this! All public methods safely handle
        connection/disconnection automatically. For testing it's still in place.
        """
        if self._con is not None:
            self._con.close()
            self._con = None
            self._cur = None

    @property
    def db_file_exists(self):
        """Lazy database existence test."""
        if self._db_file_exists:
            return True
        self._db_file_exists = os.path.isfile(self._file or '')
        return self._db_file_exists

    def _ensure_db_file_exists(self):
        if self.db_file_exists:
            return

        directory = os.path.dirname(self._file)
        os.makedirs(directory, exist_ok=True)
        with open(self._file, 'wb') as file_obj:
            file_obj.write(bytes())
        log.info('db file created: %s', self._file)

    def _fetch(self, statement, values=None):
        with self._connection() as (_, cur):
            try:
                if values is None:
                    cur.execute(statement)
                else:
                    cur.execute(statement, values)
                return cur.fetchall()

            except Exception as err:
                raise Exception(
                    'statement execution fail: "%s\nerror: %s' % (statement, err)
                )

    def _create_table(self, table):
        statement = (
            f'create table "{table}" (id integer primary key, key TEXT, value TEXT)'
        )
        log.debug('create_table statement:\n\t%s', statement)
        self._commit(statement)

    def _commit(self, statement, values=None):
        with self._connection() as (con, cur):
            try:
                if values is None:
                    cur.execute(statement)
                else:
                    cur.execute(statement, values)
                con.commit()

            except Exception as err:
                raise Exception(
                    'statement execution fail: "%s\nerror: %s' % (statement, err)
                )

    def _get_digest(self):
        with self._connection():
            tables = sorted(self.tables())
            header = ('\n\n{line}table "%s"\n  id - key - value\n{line}  ').format(
                line='-' * 40 + '\n'
            )
            text = 'database dump from %s\n' % self._file
            text += '%i tables: %s' % (len(tables), ', '.join(tables))
            for t in tables:
                statement = f'select * from "{t}"'
                data = self._fetch(statement)
                text += header % t
                text += '\n  '.join([str(i)[1:-1] for i in data])
            return text

    def log_all(self):
        """Log the complete db content."""
        log.info(self._get_digest())

    @contextmanager
    def _connection(
        self,
    ) -> Iterator[tuple[sqlite3.Connection, sqlite3.Cursor]]:
        is_owner = self._con is None
        if is_owner:
            self._con = sqlite3.connect(self._file)
            self._cur = self._con.cursor()
        try:
            yield self._con, self._cur
        finally:
            if is_owner and self._con is not None:
                self._con.close()
                self._con = None
                self._cur = None

    def _dup_check(self, table=_DEFAULT_TABLE):
        """
        Test a table for bad data. Such as double entries ...
        """
        with self._connection():
            keys = self.keys(table)
            duplicates = set(k for k in keys if keys.count(k) > 1)
            if not duplicates:
                log.info('No duplicates in db! All good!')
                return

            statement = f'select value from "{table}" where key=?'
            log.info('Cleaning up duplicate db entries in table "%s" ...', table)
            for key in duplicates:
                rows = self._fetch(statement, (key,))
                values = [json.loads(row[0]) for row in rows]
                first_entry = values[0]
                for entry in values[1:]:
                    if entry != first_entry:
                        log.warning(
                            'Removing duplicate db entry with varying data!\n  %s',
                            entry,
                        )
                self.pop(key, table)
                self.set(key, first_entry, table)
            log.info('  Done.')


if __name__ == '__main__':
    import pytest
    import test.test_a2db

    pytest.main([test.test_a2db.__file__, '-v'])
