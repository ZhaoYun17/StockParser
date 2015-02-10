# db_create.py

import sqlite3 

data=[n.split(':') for n in 'maybank:200:Financial,airasia:200:Transport,YTLREIT:500:REIT'.split(',')]



with sqlite3.connect('Dummy.db') as connection:

	# get a cursor object used to execute SQL commands
	c = connection.cursor()

	# create the table
	c.execute("""CREATE TABLE Stock
		(name TEXT NOT NULL, unit INTEGER NOT NULL, type TEXT, sector TEXT, last_value INTEGER )""")

	# insert dummy data into the table
	c.executemany(
		'INSERT INTO Stock (name, unit, sector) VALUES(?,?,?)',data
		)