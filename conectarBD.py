import psycopg2

class Conect:
    # Initialize the database object and the cursor
    def __init__(self: object):
        self.hostname = '10.0.0.1'
        self.username = 'pi'
        self.password = '####'
        self.database = '####'
        self.myConnection = psycopg2.connect(host=self.hostname, user=self.username, password=self.password, dbname=self.database)

        self.cur = self.myConnection.cursor()

    # Run a query on a database and print the results:
    def select(self: object, column: str, table: str, condition = "TRUE"):

        query = 'SELECT %s FROM %s WHERE %s' %(column, table, condition)

        self.cur.execute(query)

        results = []

        for i in self.cur.fetchall() :
            results.append(i)

        return results

    # Run a query on a database and update:
    def update(self: object, table: str, column: str, condition = "FALSE") :

        query = 'UPDATE %s SET %s WHERE %s' %(table, column, condition)

        self.cur.execute(query)

        self.myConnection.commit()

        return self.cur.rowcount

    # Closes the connection with db
    def closeCon(self: object):
        self.cur.close()
        self.myConnection.close()
