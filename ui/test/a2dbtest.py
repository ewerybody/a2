__author__ = 'eRiC'

from os.path import exists, join, abspath
#import sqlite3
#import inspect
import logging
logging.basicConfig()
log = logging.getLogger('a2dbtest')
log.setLevel(logging.DEBUG)

a2setdir = abspath(join('..', '..', 'settings', 'a2.db'))
log.debug('\n a2setdir: %s\n exists: %s' % (a2setdir, exists(a2setdir)))

import a2dblib

db = a2dblib.A2db(a2setdir)

log.info('db members:\n\t%hhs' % [d for d in dir(db) if not d.startswith('_')])
testTable = 'TEST table'
log.info('tables:\n\t%s' % db.tables())

log.info('\ntesting creating/deleting tables %s' % ('.'*40))
log.debug('testTable: "%s" Does NOT Exist: %s' % (testTable, not testTable in db.tables()))
# table creation test
db.createTable(testTable)
log.debug('testTable: "%s" Created: %s' % (testTable, testTable in db.tables()))
db.dropTable(testTable)
log.debug('testTable: "%s" Deleted: %s' % (testTable, not testTable in db.tables()))


log.info('\ntesting "set" %s' % ('.'*40))
setValue = 't32t234fsaassa'
db.set('bam', setValue, testTable)
value = db.get('bam', testTable)
log.info('value: %s' % value)
log.debug('setValue == getValue: %s' % (setValue == value))


log.info('tables: %s' % db.tables())
db.dropTable(testTable)
db._con.commit()
log.info('tables: %s' % db.tables())

db.dropTable(testTable)
log.debug('testTable: "%s" Deleted: %s' % (testTable, not testTable in db.tables()))

db.dropTable('a3')

db.all()
log.info('a2dbtest finished!')