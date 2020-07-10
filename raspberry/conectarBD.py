#!/usr/bin/python
import psycopg2

class Conect:
    # Initialize the database object and the cursor
    def __init__(self: object):
        self.hostname = '192.168.15.15'
        self.username = 'postgres'
        self.password = '####'
        self.database = '####'
        self.myConnection = psycopg2.connect(host=self.hostname, user=self.username, password=self.password, dbname=self.database)

        self.cur = self.myConnection.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS tb_arduinos(id SERIAL PRIMARY KEY, local TEXT, ip VARCHAR(15), status BOOLEAN);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS tb_currents(id SERIAL PRIMARY KEY, id_arduino INTEGER, current NUMERIC, data TIMESTAMP);")
        self.myConnection.commit()


    # Run a query on a database and print the results:
    def select(self: object, column: object, table: object, condition = "TRUE" ) :

        query = 'SELECT %s FROM %s WHERE %s' %(column, table, condition)

        self.cur.execute(query)

        results = []

        for i in self.cur.fetchall() :
            results.append(i)

        return results

    # Run a query on a database and insert the values:
    def insert(self: object, table: object, columns: object, values: object):

        listValues = values.split(",")
        listColumns = columns.split(",")

        phsColumns = ', '.join(column for column in listColumns)

        phValues= '%s'
        phsValues= ', '.join(phValues for unused in listValues)

        query= 'INSERT INTO '+table+'(%s) VALUES' % phsColumns
        
        query= query+' (%s);' % phsValues

        self.cur.execute(query, listValues)
        self.myConnection.commit()

        return ''

    # Closes the connection with db
    def closeCon(self: object):
        self.myConnection.close()
