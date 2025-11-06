#!/usr/bin/env python3
import sqlite3
import functools

# #### decorator to log SQL queries
def log_queries(func):
    """Decorator that logs SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL query: {query}")
        else:
            print("[LOG] No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# #### fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
