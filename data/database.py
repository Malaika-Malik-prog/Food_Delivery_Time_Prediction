import sqlite3
import hashlib
import secrets
import hmac

# Connect to database
def connect_db():
    return sqlite3.connect("users.db")

# Create users table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Securely hash password
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        200000
    ).hex()

    return password_hash, salt

# Register new user
def register_user(username, email, password):
    conn = connect_db()
    cursor = conn.cursor()

    password_hash, salt = hash_password(password)

    try:
        cursor.execute(
            """INSERT INTO users
            (username, email, password_hash, salt)
            VALUES (?, ?, ?, ?)""",
            (username, email, password_hash, salt)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()

# Login user
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash, salt FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return False

    stored_hash, salt = user
    entered_hash, _ = hash_password(password, salt)

    return hmac.compare_digest(stored_hash, entered_hash)
