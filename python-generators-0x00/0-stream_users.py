#!/usr/bin/python3
"""
0-stream_users.py
Generator that streams rows from the user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Connects to the ALX_prodev database and yields
    user records one by one as dictionaries.
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",   # replace with your MySQL password
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # Use only one loop (as per instructions)
        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming data: {e}")
        return
