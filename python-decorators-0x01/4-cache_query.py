#!/usr/bin/env python3
import time
import sqlite3
import functools

# Simple in-memory cache for queries
query_cache = {}


def with_db_connection(func):
    """Decorator that opens a database connection, passes it to the function, and closes it afterward"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]
        else:
            print(f"[CACHE MISS] Executing and caching result for query: {query}")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# #### First call
