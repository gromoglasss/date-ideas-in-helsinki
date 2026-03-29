from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import config

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.secret_key = config.secret_key

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def get_connection():
    conn = sqlite3.connect("database.db")
    return conn


conn = get_connection()
cursor = conn.cursor()

# mulla oli jotain ongelmia taulukkojen luomisessa niin nyt koodi luo niitä täällä myös
cursor.execute("""
CREATE TABLE IF NOT EXISTS ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    filename TEXT,
    user_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
)
""")

conn.commit()
conn.close()

# mallipohjat
def add_example_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("nea", generate_password_hash("salasana1"))
        )
        user1_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("ILikeBacon993", generate_password_hash("salasana2"))
        )
        user2_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)",
            ("Kävely", "kävely Helsingin ympäri", "stock-photo-helsinki-cityscape-with-helsinki-cathedral-and-market-square-finland.webp", user1_id)
        )

        cursor.execute(
            "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)",
            ("Kissakahvila", "Kahvitauko kissakahvilassa", "119890_cat-cafe-kissakahvila-helsinki-finland-suomi5.webp", user2_id)
        )

    conn.commit()
    conn.close()

@app.route("/")
def main():
    add_example_data()
    q = request.args.get("q", "")

    conn = get_connection()
    cursor = conn.cursor()

    if q:
        cursor.execute("""
            SELECT ideas.id, ideas.title, ideas.description, ideas.filename, ideas.user_id, users.username
            FROM ideas
            JOIN users ON ideas.user_id = users.id
            WHERE ideas.title LIKE ? OR ideas.description LIKE ?
        """, ("%" + q + "%", "%" + q + "%"))
    else:
        cursor.execute("""
            SELECT ideas.id, ideas.title, ideas.description, ideas.filename, ideas.user_id, users.username
            FROM ideas
            JOIN users ON ideas.user_id = users.id
        """)

    ideas = cursor.fetchall()
    conn.close()

    return render_template("index.html", ideas=ideas, q=q)


@app.route("/temp", methods=["GET"])
def template():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("addIdea.html")


@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    file = request.files["photo"]
    title = request.form["title"]
    message = request.form["message"]
    user_id = session["user_id"]

    filename = file.filename
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)",
        (title, message, filename, user_id)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    password_hash = generate_password_hash(password1)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "VIRHE: tunnus on jo varattu"

    conn.close()
    return redirect("/login")

@app.route("/delete/<int:idea_id>", methods=["POST"])
def delete_idea(idea_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM ideas WHERE id = ?", (idea_id,))
    idea = cursor.fetchone()

    if idea is None:
        conn.close()
        return "Idea ei löydetty"

    if idea[0] != session["user_id"]:
        conn.close()
        return "Ei oikeutta"

    cursor.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:idea_id>", methods=["GET"])
def edit_idea(idea_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, description, filename, user_id FROM ideas WHERE id = ?",
        (idea_id,)
    )
    idea = cursor.fetchone()
    conn.close()

    if idea is None:
        return "Idea ei löydetty"

    if idea[4] != session["user_id"]:
        return "Ei oikeutta"

    return render_template("editIdea.html", idea=idea)


@app.route("/update/<int:idea_id>", methods=["POST"])
def update_idea(idea_id):
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    description = request.form["message"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM ideas WHERE id = ?", (idea_id,))
    idea = cursor.fetchone()

    if idea is None:
        conn.close()
        return "Ideaa ei löydetty"

    if idea[0] != session["user_id"]:
        conn.close()
        return "Ei oikeutta"

    cursor.execute(
        "UPDATE ideas SET title = ?, description = ? WHERE id = ?",
        (title, description, idea_id)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth.html")

    username = request.form["username"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return "VIRHE: väärä tunnus tai salasana"

    if not check_password_hash(user[1], password):
        return "VIRHE: väärä tunnus tai salasana"

    session["user_id"] = user[0]
    session["username"] = username
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")