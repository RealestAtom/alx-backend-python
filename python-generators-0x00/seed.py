#!/usr/bin/python3
"""
seed.py
Sets up the ALX_prodev MySQL database, creates user_data table,
and loads data from a CSV file.
Includes a generator that streams rows from the table one by one.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid

# ----------------------------
# 1️⃣ Connect to MySQL Server
# ----------------------------
def connect_db():
    """Connect to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"   # Change this to your MySQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ----------------------------
# 2️⃣ Create Database
# ----------------------------
def create_database(connection):
    """Create database ALX_prodev if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

# ----------------------------
# 3️⃣ Connect to ALX_prodev
# ----------------------------
def connect_to_prodev():
    """Connect directly to ALX_prodev"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",   # Change this to your MySQL password
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

# ----------------------------
# 4️⃣ Create user_data table
# ----------------------------
def create_table(connection):
    """Create user_data table if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,2) NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

# ----------------------------
# 5️⃣ Insert CSV Data
# ----------------------------
def insert_data(connection, csv_file):
    """Insert data from CSV file into user_data table"""
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Generate UUID if not present
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age);
                """, (user_id, name, email, age))
        connection.commit()
        print(f"Data from {csv_file} inserted successfully.")
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")

# ----------------------------
# 6️⃣ Generator to stream rows
# ----------------------------
def stream_user_data(connection):
    """Generator that streams user_data rows one by one"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
        cursor.close()
    except Error as e:
        print(f"Error streaming data: {e}")
        return

# Example use (uncomment for testing)
# if __name__ == "__main__":
#     conn = connect_to_prodev()
#     for row in stream_user_data(conn):
#         print(row)
