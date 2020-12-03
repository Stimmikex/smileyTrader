import sqlite3

class Database:
    """Database singleton class for our smileycoin trader"""

    __instance = None
    def __new__(cls, *args, **kwargs):
        """Singleton generator for the Database class"""
        if not cls.__instance:
            cls.__instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls.__instance.conn = sqlite3.connect('database.db')
            cls.__instance.c = cls.__instance.conn.cursor()
        return cls.__instance

    def __init__(self):
        """Constructor for our database and database class instance."""
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS User (
                username text NOT NULL,
                password text NOT NULL,
                credits integer NOT NULL,
                pubKey text NOT NULL,
                priKey text NOT NULL
            )""")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                name text NOT NULL,
                price integer NOT NULL
            )""")
        self.conn.commit()

    def selectSQL(self, query):
        """Generic select and return function for the database."""
        self.c.execute(query)
        return self.c.fetchall()[0][0]

    def insertSQL(self, query):
        """Generic insert and/or update function for the database."""
        self.c.execute(query)
        self.conn.commit()

    def cleanup(self):
        """Cleans the database, shrinking it's size."""
        self.conn.execute('VACUUM')
