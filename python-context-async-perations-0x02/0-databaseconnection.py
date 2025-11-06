#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """Custom context manager to handle opening and closing of database connections"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection and return the connection object"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection, handling errors if they occur"""
        if self.conn:
            if exc_type is not None:
                # Optional rollback if an exception occurs
                self.conn.rollback()
            self.conn.close()


# #### Example usage of the context manager
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
