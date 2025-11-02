#!/usr/bin/python3
"""
1-batch_processing.py
Create a generator to fetch and process user data in batches.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from user_data table in batches.
    Each yield returns a list of user dictionaries.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # change this to your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        batch = []
        # Loop through all rows
        for row in cursor:
            batch.append(row)
            # When batch is full, yield and reset
            if len(batch) == batch_size:
                yield batch
                batch = []

        # Yield the remaining rows if they exist
        if batch:
            yield batch

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming batches: {e}")
        return


def batch_processing(batch_size):
    """
    Processes each batch fetched from stream_users_in_batches().
    Filters users over age 25 and prints them.
    Uses yield for streaming output.
    """
    # Loop over the batches
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25
        filtered_users = [user for user in batch if float(user['age']) > 25]

        # Yield each filtered user
        for user in filtered_users:
            yield user


# Run when file executed directly (for debugging)
if __name__ == "__main__":
    for user in batch_processing(50):
        print(user)
