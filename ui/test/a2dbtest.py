__author__ = 'eRiC'

from os.path import exists, join, abspath
#import sqlite3
#import inspect
import json
import logging
logging.basicConfig()
log = logging.getLogger('a2dbtest')
log.setLevel(logging.DEBUG)

a2setdir = abspath(join('..', '..', 'settings', 'a2.db'))
log.debug('\n a2setdir: %s\n exists: %s' % (a2setdir, exists(a2setdir)))

import a2dblib
db = a2dblib.A2db(a2setdir)

log.info('db members:\n\t%s' % [d for d in dir(db) if not d.startswith('_')])
testTable = 'TEST table'

log.info('\ntesting creating/deleting tables %s' % ('.' * 40))
log.debug('testTable: "%s" Does NOT Exist: %s' % (testTable, testTable not in db.tables()))
db.createTable(testTable)
log.debug('testTable: "%s" Created: %s' % (testTable, testTable in db.tables()))
db.dropTable(testTable)
log.debug('testTable: "%s" Deleted: %s' % (testTable, testTable not in db.tables()))


log.info('\ntesting "set" %s' % ('.' * 40))
setValue = 't32t234fsaassa'
db.set('bam', setValue, testTable)
value = db.get('bam', testTable)
log.info('value: %s' % value)
log.debug('setValue == getValue: %s' % (setValue == value))


log.info('tables: %s' % db.tables())
db.dropTable(testTable)
db._con.commit()
log.info('tables: %s' % db.tables())

log.info('\ntesting getting/setting dictionaries with JSON %s' % ('.' * 40))
d = {'name': [1, 2, 3], 'bla': {'alist': ['&\323@!|//'], 'value': 123.523452}}
log.info('d: %s' % d)
#j = json.dumps(d, separators=(',', ':'))
#log.info('j: %s - %s' % (j, type(j)))
db.set('jsonTest', d, testTable)
x = db.get('jsonTest', testTable)
log.info('x: %s' % x)
dx = json.loads(x)
log.info('dx: %s' % dx)
log.info('dx == d: %s' % (dx == d))
dd = db.getd('jsonTest', testTable)
log.info('d == dd: %s' % (d == dd))

log.info('\ndeleting values ".pop" %s' % ('.' * 40))
key = 'jsonTest'
log.info('key exists: %s' % (key in db.keys(testTable)))
db.pop('jsonTest', testTable)
log.info('key deleted: %s' % (key not in db.keys(testTable)))


db.dropTable(testTable)
log.debug('testTable: "%s" Deleted: %s' % (testTable, testTable not in db.tables()))

db.dropTable('a3')

#db.all()
log.info('a2dbtest finished!')
