from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

def create_user(username, password):
    conn = get_connection()

    password_hash = generate_password_hash(password)

    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )

    conn.commit()
    conn.close()

def check_login(username, password):
    conn = get_connection()

    user = conn.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if not user:
        return None

    if check_password_hash(user["password_hash"], password):
        return user["id"]

    return None

def get_username(user_id):
    conn = get_connection()

    user = conn.execute(
        "SELECT username FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if user:
        return user["username"]
    return None