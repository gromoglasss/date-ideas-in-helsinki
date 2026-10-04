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

def get_user(user_id):
    conn = get_connection()

    user = conn.execute(
        "SELECT id, username FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    conn.close()
    return user

def get_ideas(user_id):
    conn = get_connection()

    ideas = conn.execute(
        "SELECT id, title FROM ideas WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    conn.close()
    return ideas

def get_stats(user_id):
    conn = get_connection()

    idea_count = conn.execute(
        "SELECT COUNT(id) FROM ideas WHERE user_id = ?",
        (user_id,)
    ).fetchone()[0]

    comment_count = conn.execute(
        "SELECT COUNT(id) FROM comments WHERE user_id = ?",
        (user_id,)
    ).fetchone()[0]

    conn.close()
    return {"idea_count": idea_count, "comment_count": comment_count}
