import sqlite3
import config
from werkzeug.security import generate_password_hash

#esimerkki-ideat
def seed_example_data():
    conn = get_connection()

    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    idea_count = conn.execute("SELECT COUNT(*) FROM ideas").fetchone()[0]

    if user_count == 0 and idea_count == 0:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("maija", generate_password_hash("salasana1"))
        )
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("pekka", generate_password_hash("salasana2"))
        )

        maija_id = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            ("maija",)
        ).fetchone()[0]

        pekka_id = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            ("pekka",)
        ).fetchone()[0]

        conn.execute(
            "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)",
            ("Ensimmäinen idea", "Tämä on esimerkkidea.", "", maija_id)
        )

        conn.execute(
            "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)",
            ("Toinen idea", "Tässä on toinen esimerkkidea.", "", pekka_id)
        )

    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect(config.database_file)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    with open("schema.sql") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()