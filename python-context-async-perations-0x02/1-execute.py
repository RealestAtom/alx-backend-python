#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """Custom context manager to handle both database connection and query execution"""
    
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open the database connection, execute the query, and return the results"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the connection is closed properly, even on error"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


# #### Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print(results)
