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
            CREATE TABLE IF NOT EXISTS Users (
                username text NOT NULL UNIQUE,
                password text NOT NULL,
                credits integer NOT NULL,
                pubKey text NOT NULL,
                privKey text NOT NULL
            )""")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                name text NOT NULL UNIQUE,
                price integer NOT NULL,
                quantity integer NOT NULL
            )""")
        self.conn.commit()

    def selectSQL(self, query, values=None):
        """Generic select and return function for the database."""
        if values:
            self.c.execute(query, values)
        else:
            self.c.execute(query)
        return self.c.fetchall()

    def insertSQL(self, query, values):
        """Generic insert and/or update function for the database."""
        self.c.execute(query, values)
        self.conn.commit()

    def existsSQL(self, table, column, value):
        """Checks if a table in a column contains a value."""
        self.c.execute(f"SELECT EXISTS (SELECT 1 FROM {table.capitalize()} WHERE {column} = (?))", (value,))
        if self.c.fetchall()[0][0] == 1:
            return True
        else:
            return False

    def cleanup(self):
        """Cleans the database, shrinking it's size."""
        self.conn.execute('VACUUM')
