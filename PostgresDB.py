import psycopg2


class PostgresDB:
    def __init__(self, user, password):
        self.host = ""
        self.port = ""
        self.dbname = ""
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connection to database successful")
        except Exception as e:
            print(f"Unable to connect to the database: {str(e)}")
            raise

    def close(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Unable to execute query: {str(e)}")
            raise
