import sqlite3
import hashlib
import os

DB_PATH = "data/users.db"

# ---------------- DB INIT ---------------- #

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ---------------- HELPERS ---------------- #

def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- CHECK EXISTING USER ---------------- #

def has_user():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count > 0

# ---------------- CREATE USER ---------------- #

def create_user(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, _hash(password))
        )

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        return False

# ---------------- VERIFY USER ---------------- #

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )

    row = c.fetchone()
    conn.close()

    if not row:
        return False

    return row[0] == _hash(password)

# ---------------- GET USER ---------------- #

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    row = c.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "username": row[0]
    }
