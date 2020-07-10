#!/usr/bin/python

class Conect:
	def __init__(self):
		import psycopg2

		self.hostname = '10.0.0.1'
		self.username = 'pi'
		self.password = 'currentM'
		self.database = 'ENERGY_MANAGER'
		self.myConnection = psycopg2.connect(host=self.hostname, user=self.username, password=self.password, dbname=self.database)

		self.cur = self.myConnection.cursor()

	# Simple routine to run a query on a database and print the results:
	def select( self, column, table, condition = "TRUE") :

		query = 'SELECT %s FROM %s WHERE %s' %(column, table, condition)

		self.cur.execute(query)

		results = []

		for i in self.cur.fetchall() :
			results.append(i)

		return results

	# Simple routine to run a query on a database and update:
	def update( self, table, column, condition = "FALSE") :

		query = 'UPDATE %s SET %s WHERE %s' %(table, column, condition)

		results = self.cur.execute(query)

		self.myConnection.commit()

		return self.cur.rowcount

	def closeCon(self):
		self.cur.close()
		self.myConnection.close()
