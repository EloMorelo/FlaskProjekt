import hashlib
import os
import sys
import sqlite3


DB_NAME = "users.db"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_user(username: str, password: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash) VALUES(?, ?)
                       """,(username, password_hash))
        conn.commit()
        print(f"Added user: {username}")
    except sqlite3.IntegrityError:
        print(f"User: {username} already exists")
    finally:
        conn.close()


def main():
    init_db()

    add_user("admin", "admin")
    add_user("user", "user")


if __name__ == "__main__":
    sys.exit(main())
