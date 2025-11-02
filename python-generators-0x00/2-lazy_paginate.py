#!/usr/bin/python3
"""
2-lazy_paginate.py
Implements lazy pagination using a generator to fetch pages only when needed.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a specific page of users from user_data table
    based on the given page size and offset.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches paginated data.
    Fetches the next page only when needed.
    Uses only one loop.
    """
    offset = 0
    while True:  # one main loop
        page = paginate_users(page_size, offset)
        if not page:
            break  # stop when no more results
        yield page  # yield one page (list of dicts)
        offset += page_size
