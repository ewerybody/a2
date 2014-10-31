'''
crySql - a couple of sql wrappers to make simple, scriptfriendly use
of an sql database without dealing with the SQL talk.

Basically what we want is pushing data to it:
crySql.add( thisData, thisTable, thisDb )

'''
__author__ = 'eric'
__version__= 0.1

import sqlite3

class CrySql(object):
	'''
	Humble sqlite3 wrapper object that holds the actual sql connection,
	a cursor already and some handy variables. Saves a couple of lines.
	'''
	def __init__(self):
		self.con = None
		self.cur = None
		self.quickConnect = False
		self.dbFile = None

	def connect( self, dbFile, quick ):
		self.dbFile = dbFile
		self.con = sqlite3.connect( dbFile )
		self.cur = self.con.cursor()
		self.quickConnect = quick

	def close(self):
		self.cur.close()
		self.con.close()
		self.dbFile = None
		self.quickConnect = False

	def quickRelease(self):
		if self.quickConnect:
			self.close()


def connect( connection, quick=False ):
	'''
	Shorthand method to just return a crySql object.
	You can give it a filepath to database file or a file that you want to have crated
	or a crySql object. This will just be returned.

	:param dbFile: string path to database file OR previously created CrySql object
	:type dbFile: str or CrySql object
	:param quick: marks the CrySql object as quick connected so its released after use
	:type quick: bool
	
	Example:
	>>> import crySql
	>>> testDb = crySql.connect( dbFile )
	
	@author eric
	@version: 0.3
	'''
	# just return the CrySql object if its established
	if isinstance( connection, CrySql ):
		connection.quickConnect = False
		return connection
	# otherwise create a new CrySql obj and connect
	else:
		crySqlObj = CrySql()
		crySqlObj.connect( connection, quick )
		return crySqlObj


def add( data, table, connection ):
	'''
	Add a chunk of data to a table in the database.
	If either the table or the database don't exist they will be created.
	The table will be made out of the types put in the dictionary items.
	
	:param data: dictionary with columnHeaderName and value pairs
	:type data: dict
	:param table: a table name
	:type table: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	
	Example
	>>> import crySql
	>>> crySql.add( {'Name':'greg','number':99}, 'names', '//fs1/bla/test.db' )
	
	@author eric
	'''
	checkData(data)
	connection = connect( connection, quick=True )
	# make sure table exists
	tableCreated = checkTable( data, table, connection )
	# make sure column exists
	if not tableCreated:
		checkColumns( data, table, connection )
	#connection.cur.executemany("INSERT INTO Friends VALUES( ?, ?, ? )", d)
	# "INSERT INTO " + table + "(Name) VALUES ('Rebecca')"
	# "INSERT INTO " + table + "(Name,Other) VALUES ('Rebecca','lalala')"
	statement = "INSERT INTO '" + table + "' ("
	statement += ','.join(data.keys()) + ") VALUES "
	statement += '(' + str(data.values())[1:-1] + ')'
	#print( 'statement: ' + str(statement) )
	execute( statement, connection )
	connection.con.commit()
	connection.quickRelease()


def query( statement, connection ):
	'''
	sql query statement wrapper for all the fetchall cases
	for inline use: give it a db-filename it establishes and releases connections itself
	give a CrySql object and it will use this and keep it alive
	
	:param statement: a valid SQL statement that can be fetched via cur.fetchall()
	:type statement: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	
	@author eric
	'''
	connection = connect( connection, quick=True )
	# execute statement and get data
	execute( statement, connection )
	data = connection.cur.fetchall()
	# shut down connection if needed
	connection.quickRelease()
	# spit out data
	return data


def set( data, table, connection, where=('Id','1') ):
	'''
	To set a single values in a table.
	By default the one in the first row of a column
	If the column does not exist yet, it will be created
	
	:param data: dictionary with columnHeaderName and value pairs
	:type data: dict
	:param table: a table name
	:type table: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	:param where: if not stated otherwise this will set the data in the row where Id = 1
	:type where: str tuple
	'''
	checkData(data)
	connection = connect( connection, quick=True )
	# make sure table exists
	tableCreated = checkTable( data, table, connection )
	# test if column exists if table was not freshly created
	if not tableCreated:
		checkColumns( data, table, connection )
	# make sure the row exists
	if tableCreated or where[1] not in get( where[0], table, connection ):
		# assemble the insert statenent
		statement = "INSERT OR REPLACE INTO '" + table + "' (Id"
		for key in data: statement += ', ' + key
		statement += ") VALUES (1"
		for key in data: statement += ", '" + str(data[key]) + "'"
		statement += ')'
	else:
		statement = "UPDATE '" + table + "' SET "
		statement += ", ".join( [ "'" + k + "'='" + str(data[k]) + "'" for k in data ] )
		statement += " WHERE " + where[0] + "=" + where[1]
	#print( 'statement: ' + str(statement) )
	execute( statement, connection )
	connection.con.commit()
	connection.quickRelease()


def checkTable( data, table, connection ):
	changed = False
	connection = connect( connection, quick=True )
	if table not in getTableNames( connection ):
		changed = True
		# create statement made of dictionary keys and value types
		statement = 'CREATE TABLE "' + table + '" (Id INTEGER PRIMARY KEY'
		for key in data:
			statement += ', ' + key + ' ' + pyTypeToSql( data[key] )
		statement += ')'
		#print( 'statement: ' + str(statement) )
		execute( statement, connection )
	connection.quickRelease()
	return changed


def checkColumns( data, table, connection ):
	changed = False
	connection = connect( connection, quick=True )
	existingColumns = [ i[1] for i in getTableInfo( table, connection ) ]
	for k in data:
		if k not in existingColumns:
			execute( "ALTER TABLE '" + table + "' ADD COLUMN " + k + " " + pyTypeToSql( data[k]), connection )
			changed = True
	connection.quickRelease()
	return changed


def dropTable( tables, connection ):
	connection = connect( connection, quick=True )
	if isinstance( tables, basestring ): tables = [tables]
	currentTables = getTableNames( connection )
	touched = False
	for table in tables:
		if table in currentTables:
			execute( 'DROP TABLE "' + table + '"', connection )
			touched = True
	if touched:
		connection.con.commit()
	connection.quickRelease()


def get( column, table, connection, raw=False ):
	'''
	Fetches data array from a given column
	As sqlite would always return tuples this can strip elements
	to a flat list if only a single column is queried.
	
	:param column: column haeader name
	:type column: str
	:param table: the table name
	:type table: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	:param raw: false by default, strips elements from 1 element tuples. If true return data is untouched
	:type raw: bool
	
	Example:
	>>> names = crySql.get( 'names', 'aTable', db )

	@author eric
	'''
	connection = connect( connection, quick=True )
	statement = "SELECT " + column + " FROM " + table
	#print( 'statement: ' + str(statement) )
	data = query( statement, connection )
	connection.quickRelease()
	# if single column querried: strips content from 1 element tuples
	if not raw:
		if not ',' in column:
			data = [i[0] for i in data]
	return data


def getTableNames( connection ):
	'''
	get all table names from db
	
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	
	Example:
	>>> getTableNames( db )
	
	@author eric
	'''
	names = query( "SELECT name FROM sqlite_master WHERE type='table'", connection )
	for i in range(len(names)):
		names[i] = names[i][0]
	return names


def getTableInfo( table, connection ):
	'''
	get the table column names and format in a list of tuples with ( index, name, data type, ... )
	
	:param table: a table name
	:type table: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	
	Example
	>>> getTableInfo( 'Friends', connection )
	
	@author eric
	'''
	info = query( 'PRAGMA table_info(' + table + ')', connection )
	return info


def getAll( table, connection ):
	'''
	get all rows from a given table
	
	:param table: a table name
	:type table: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	
	Example
	>>> getRows( table, db )
	
	@author eric
	'''
	rows = query( 'SELECT * FROM %s ' % table, connection )
	return rows


def pyTypeToSql( element ):
	'''
	takes an object an returns its type in SQL terms if it can be identified
	
	:param element: a string, float or integer 
	:type element: str, float or int
	
	Returns:
		(str) string
	
	Example
	>>> pyTypeToSql( 'A string!' )
	>>> 'TEXT'
	
	@author eric
	'''
	if isinstance( element, basestring ):
		return 'TEXT'
	if isinstance( element, float ):
		return 'REAL'
	if isinstance( element, int ):
		return 'INT'
	else:
		raise IOError, 'type of "' + str(element) + '" not handled yet!'


def execute( statement, connection ):
	'''
	error checking execute function
	
	:param statement: a valid SQL statement that can be fetched via cur.fetchall()
	:type statement: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	
	@author eric
	'''
	#print( 'executing statement: ' + str(statement) )
	connection = connect( connection, quick=True )
	try:
		connection.cur.execute( statement )
	except Exception, err:
		connection.quickRelease()
		raise IOError, 'crySql failed to execute statement: "' + statement + '"'
	connection.quickRelease()


def delete( index, table, connection ):
	'''
	deletes a row with a certain index
	
	:param index: number of row in Id column
	:type index: int
	:param table: table name
	:type table: str
	:param connection: a path do a database file or an already connected crySql object
	:type connection: str or crySql obj
	'''
	connection = connect( connection, quick=True )
	execute( "DELETE FROM " + table + " WHERE Id='" + str(index) + "'", connection )
	connection.con.commit()
	connection.quickRelease()


def checkData( data ):
	'''
	single line check for if data is a dict
	
	:param data: a proper dictionary with key:value pairs
	:type data: dict
	'''
	if not isinstance(data, dict):
		print( 'data: ' + str(data) )
		raise IOError, 'crySql: type of "' + str(data) + '" not a dict!'