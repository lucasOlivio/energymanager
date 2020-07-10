#!/usr/bin/python

class Conect:
    def __init__(self):
        import psycopg2

        self.hostname = '192.168.15.15'
        self.username = 'postgres'
        self.password = 'lukinhasoli23'
        self.database = 'ENERGY_MANAGER'
        self.myConnection = psycopg2.connect(host=self.hostname, user=self.username, password=self.password, dbname=self.database)

        self.cur = self.myConnection.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS tb_arduinos(id SERIAL PRIMARY KEY, local TEXT, ip VARCHAR(15), status BOOLEAN);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS tb_currents(id SERIAL PRIMARY KEY, id_arduino INTEGER, current NUMERIC, data TIMESTAMP);")
        self.myConnection.commit()


    # Simple routine to run a query on a database and print the results:
    def select( self, column, table, condition = "TRUE" ) :

        #listParameters = []

        #listColumns = column.split(",")

        #listParameters.append(clm for clm in listColumns)

        #phColumns = '%s'
        #phsColumns = ', '.join(phColumns for unused in listColumns)

        #phConditions = '%s'
        #phsConditions = ' '.join(phConditions for unused in listConditions)

        query = 'SELECT %s FROM %s WHERE %s' %(column, table, condition)

        #print(query)

        self.cur.execute(query)

        results = []

        for i in self.cur.fetchall() :
            results.append(i)

        return results

    def insert(self, table, columns, values):

        listValues = values.split(",")
        listColumns = columns.split(",")

        phsColumns = ', '.join(column for column in listColumns)

        phValues= '%s'
        phsValues= ', '.join(phValues for unused in listValues)

        query= 'INSERT INTO '+table+'(%s) VALUES' % phsColumns
        
        query= query+' (%s);' % phsValues

        #print(query)
        resp = self.cur.execute(query, listValues)
        self.myConnection.commit()

        return ''


    def closeCon(self):
        self.myConnection.close()
