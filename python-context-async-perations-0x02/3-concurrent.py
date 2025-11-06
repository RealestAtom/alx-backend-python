#!/usr/bin/env python3
import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users


async def fetch_concurrently():
    """Run both database queries concurrently"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    all_users, older_users = results
    print("All Users:")
    print(all_users)
    print("\nUsers older than 40:")
    print(older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
