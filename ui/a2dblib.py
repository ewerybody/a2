"""
a2dblib - wrapper to the a2 database

Mainly we store key value pairs. So the 'tables' are more or less
lets see how we deal with 'real' tables in the future... if we need to

id key  value
-------------
01 this 0.5
02 that 'lala'
03 blib 'something'
04 blob 'something'

this enables us to do simple get/set things like

incls = a2db.get('includes', 'a2')
a2db.set('includes', 'a2', incls)
a2db.rem('tempstuff', 'a2')

TODO: replace those 'string ' + var + ' string' statements with
    'string % string' % var
"""
import os
import sqlite3
#import logging
import fakeLog as logging
log = logging.getLogger(__name__)


class A2db:
    def __init__(self, a2dbFile):
        self.file = a2dbFile
        self.con = sqlite3.connect(a2dbFile)
        self.cur = self.con.cursor()
        log.info('A2db initialised! (%s)' % self.file)

    def get(self, key, table='a2'):
        """
        Gets you a value from a keyName and tableName.

        This correctly triggers the key error because fetch silently returns [] if key is not
        available. So return [0] fails! And not fetch. But ok thats good :]
        :param key: keyName in the "key" column
        :param table: tableName
        :return: string of the data or empty string
        """
        try:
            data = self.fetch('select value from %s where key="%s"' % (table, key))
            return data[0][0]
        except:
            if table not in self.tables():
                log.error('there is no table named "%s"' % table)
                return ''
            elif key not in self.keys(table):
                log.error('there is no key "%s" in section "%s"' % (key, table))
                return ''

    def set(self, key, value, table='a2', check=False):
        """
        example:
        update TableName SET valueName=value WHERE key=keyName
        """
        try:
            if not key in self.keys(table):
                statement = ('insert into %s ("key","value") values ("%s", "%s")' % (table, key, value))
            else:
                statement = 'update %s set value="%s" WHERE key="%s"' % (table, value, key)
            self.execute(statement)
            self.con.commit()
        except:
            if not table in self.tables():
                self.checkTable(table)
                self.set(key, value, table)
            else:
                log.error('could not set value: "%s" on key:"%s" in section:"%s"' % (value, key, table))

    def tables(self):
        tablelist = self.fetch("SELECT name FROM sqlite_master WHERE type='table'")
        return [t[0] for t in tablelist]

    def keys(self, table='a2'):
        data = self.fetch('select key from %s' % table)
        return [k[0] for k in data]

    def fetch(self, statement):
        self.execute(statement)
        return self.cur.fetchall()

    def checkTable(self, table):
        if table not in self.tables():
            dirty = True
            statement = 'create table "%s" (id integer primary key, key TEXT, value TEXT)' % table
            self.execute(statement)
            return False
        return True

    def execute(self, statement):
        try:
            self.cur.execute(statement)
        except Exception as err:
            raise Exception('statement execution fail: "%s\nerror: %s' % (statement, err))

    def all(self):
        tables = self.tables()
        for t in tables:
            columns = ' - '.join([i[1] for i in self.fetch('PRAGMA table_info("%s")' % t)])
            print('\ntable: "%s":\n  %s\n  %s\n  %s' % (t, columns, '-'*40,
                '\n  '.join([str(i)[1:-1] for i in self.fetch('select * from "%s"' % t)])))


    # old crap --------------------------------------------------------

    def oldset(self, data, section, where=('Id', '1')):
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
        self.execute(statement)

    def getSqlType(self, element):
        if isinstance(element, str):
            return 'TEXT'
        elif isinstance(element, float):
            return 'REAL'
        elif isinstance(element, int):
            return 'INT'
        else:
            raise IOError('type of "' + str(element) + '" not handled yet!')

    def oldcheckSections(self, data, section):
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
            self.execute(statement)
        else:
            # according to given data.keys() check for column existance
            tableNfo = self.fetch('PRAGMA table_info(%s)' % section)
            columns = [i[1] for i in tableNfo]
            for key in data:
                if key in columns:
                    continue
                self.execute("ALTER TABLE '" + section + "' ADD COLUMN " + key + " " + self.getSqlType(data[key]))
                isDirty = True
        return isDirty

    def oldget(self, column, section):
        statement = "SELECT %s FROM %s" % (column, section)
        data = []
        try:
            data = self.fetch(statement)
        except:
            log.error('could not get data from db "%s" in section "%s"' % (column, section))
        # if not raw:
        #	if not ',' in column:
        #		data = [i[0] for i in data]
        return data

    def add(self, data, section):
        self.checkTable(section)
        statement = "INSERT INTO '" + section + "' ("
        statement += ','.join(data.keys()) + ") VALUES "
        statement += '(' + str(data.values())[1:-1] + ')'

        "INSERT INTO %s (%s) VALUES (%s)" % ()

        print( 'statement: ' + str(statement) )
        self.execute(statement)
        self.con.commit()


def check(a2obj):
    a2dbFile = os.path.join(a2obj.a2setdir, 'a2.db')
    db = A2db(a2dbFile)
    return db
