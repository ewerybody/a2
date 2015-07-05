"""
a2dblib - wrapper to the a2 database

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
import sqlite3
import logging
logging.basicConfig()
log = logging.getLogger('a2db')
log.setLevel(logging.INFO)

_defaultTable = 'a2'
_defaultSep = '|'


class A2db(object):
    def __init__(self, a2dbFile):
        self._file = a2dbFile
        self._con = sqlite3.connect(a2dbFile)
        self._cur = self._con.cursor()
        log.info('database initialised! (%s)' % self._file)

    def get(self, key, table=_defaultTable):
        """
        Gets you a value from a keyName and tableName.

        This correctly triggers the key error because fetch silently returns [] if key is not
        available. So return [0] fails! And not fetch. But ok thats good :]
        :param key: keyName in the "key" column
        :param table: tableName
        :return: string of the data or empty string
        """
        try:
            data = self._fetch('select value from "%s" where key="%s"' % (table, key))
            return data[0][0]
        except:
            if table not in self.tables():
                log.error('there is no table named "%s"' % table)
                return ''
            elif key not in self.keys(table):
                log.error('there is no key "%s" in section "%s"' % (key, table))
                return ''

    def gets(self, key, table=_defaultTable, sep=_defaultSep):
        """
        returns a separated list from a db string entry
        """
        value = self.get(key, table)
        if not value:
            return set()
        return set(value.split(sep))

    def set(self, key, value, table=_defaultTable, sep=_defaultSep, check=False):
        """
        update TableName SET valueName=value WHERE key=keyName
        example:
        """
        # to accept iterable values make them a string with separators
        if isinstance(value, (set, list, tuple)):
            value = sep.join(value)
        
        try:
            if key not in self.keys(table):
                statement = ('insert into "%s" ("key","value") values ("%s", "%s")' % (table, key, value))
                log.debug('adding value!\n  %s' % statement)
            else:
                statement = 'update "%s" set value="%s" WHERE key="%s"' % (table, value, key)
                log.debug('updating value!\n  %s' % statement)
            self._execute(statement)
            self._con.commit()
        #except sqlite3.DatabaseError as error:
        except:
            log.debug('setting db failed...')
            if table not in self.tables():
                log.debug('creating table and retry...')
                self.createTable(table)
                # TODO: resolve loop:
                self.set(key, value, table)
            else:
                #log.error('could not set value: "%s" on key:"%s" in section:"%s"\n%s' % (value, key, table, error))
                log.error('could not set value: "%s" on key:"%s" in section:"%s"' % (value, key, table))

    def adds(self, key, value, table=_defaultTable, sep=_defaultSep):
        """
        appends a string value to a string entry with a separator if its not already in
        should basically work like built-in set.add
        """
        current = self.gets(key, table, sep)
        if '' in current:
            current.remove('')
        
        if value not in current:
            current.add(value)
            self.set(key, sep.join(current), table)
            log.debug('added "%s" to key:%s - %s' % (value, key, current))
        return current

    def dels(self, key, value, table=_defaultTable, sep=_defaultSep):
        """
        deletes a string value from an entry
        """
        current = self.gets(key, table, sep)
        if value in current:
            current.remove(value)
            self.set(key, sep.join(current), table)
            log.debug('deleted "%s" to key:%s - %s' % (value, key, current))
        return current

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
            #log.error('statement execution fail: "%s\nerror: %s' % (statement, err))

    def all(self):
        tables = self.tables()
        for t in tables:
            columns = ' - '.join([i[1] for i in self._fetch('PRAGMA table_info("%s")' % t)])
            log.info('\ntable: "%s":\n  %s\n  %s\n  %s' % (t, columns, '-' * 40, '\n  '.join([str(i)[1:-1] for i in self._fetch('select * from "%s"' % t)])))

    # old crap --------------------------------------------------------

    def _oldset(self, data, section, where=('Id', '1')):
        """
        example:
        INSERT OR REPLACE INTO TableName (Id, key) VALUES (1,value)
        """
        changed = self.checkSections(data, section)
        if changed or where[1] not in self.get(where[0], section):
            # assemble the insert statenent
            statement = "INSERT OR REPLACE INTO '" + section + "' (Id"
            for key in data:
                statement += ', ' + key
            statement += ") VALUES (1"
            for key in data:
                statement += ", '" + str(data[key]) + "'"
            statement += ')'
        else:
            statement = "UPDATE '" + section + "' SET "
            statement += ", ".join(["'" + k + "'='" + str(data[k]) + "'" for k in data])
            statement += " WHERE " + where[0] + "=" + where[1]
        self._execute(statement)

    def _getSqlType(self, element):
        if isinstance(element, str):
            return 'TEXT'
        elif isinstance(element, float):
            return 'REAL'
        elif isinstance(element, int):
            return 'INT'
        else:
            raise IOError('type of "' + str(element) + '" not handled yet!')

    def _oldcheckSections(self, data, section):
        """
        for longer tables this checks the number of columns so the given data fits
        """
        isDirty = False
        if section not in self.getSections():
            # section not in db at all? create it with columns from data types
            isDirty = True
            statement = 'CREATE TABLE "' + section + '" (Id INTEGER PRIMARY KEY'
            for key in data:
                statement += ', ' + key + ' ' + self.getSqlType(data[key])
            statement += ')'
            self._execute(statement)
        else:
            # according to given data.keys() check for column existance
            tableNfo = self._fetch('PRAGMA table_info(%s)' % section)
            columns = [i[1] for i in tableNfo]
            for key in data:
                if key in columns:
                    continue
                self._execute("ALTER TABLE '" + section + "' ADD COLUMN " + key + " " + self.getSqlType(data[key]))
                isDirty = True
        return isDirty

    def _oldget(self, column, section):
        statement = "SELECT %s FROM %s" % (column, section)
        data = []
        try:
            data = self._fetch(statement)
        except:
            log.error('could not get data from db "%s" in section "%s"' % (column, section))
        # if not raw:
        #	if not ',' in column:
        #		data = [i[0] for i in data]
        return data

    def _add(self, data, section):
        """
        depricated
        """
        self.checkTable(section)
        statement = "INSERT INTO '" + section + "' ("
        statement += ','.join(data.keys()) + ") VALUES "
        statement += '(' + str(data.values())[1:-1] + ')'

        "INSERT INTO %s (%s) VALUES (%s)" % ()

        print('statement: ' + str(statement))
        self._execute(statement)
        self._con.commit()
