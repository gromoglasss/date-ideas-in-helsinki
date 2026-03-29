import os
import sqlite3
from flask import Flask, redirect, render_template, request, session
import config
import db
import ideas
import users

app = Flask(__name__)
app.secret_key = config.secret_key
app.config["UPLOAD_FOLDER"] = "static/uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
#esimerkki-ideoiden lisäys
db.init_db()
db.seed_example_data()


@app.route("/")
def index():
    query = request.args.get("q", "")
    all_ideas = ideas.get_ideas(query)
    return render_template("index.html", ideas=all_ideas, q=query)


@app.route("/temp")
def show_add_form():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("addIdea.html")


@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    description = request.form["message"]
    file = request.files["photo"]

    filename = ""
    if file and file.filename:
        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

    ideas.add_idea(title, description, filename, session["user_id"])
    return redirect("/")


@app.route("/edit/<int:idea_id>", methods=["GET", "POST"])
def edit_idea(idea_id):
    if "user_id" not in session:
        return redirect("/login")

    idea = ideas.get_idea(idea_id)
    if not idea:
        return "VIRHE: ideaa ei löytynyt"

    if idea["user_id"] != session["user_id"]:
        return "VIRHE: ei oikeutta muokata tätä ideaa"

    if request.method == "GET":
        return render_template("editIdea.html", idea=idea)

    title = request.form["title"]
    description = request.form["message"]
    ideas.update_idea(idea_id, title, description)
    return redirect("/")


@app.route("/delete/<int:idea_id>", methods=["POST"])
def delete_idea(idea_id):
    if "user_id" not in session:
        return redirect("/login")

    idea = ideas.get_idea(idea_id)
    if not idea:
        return "VIRHE: ideaa ei löytynyt"

    if idea["user_id"] != session["user_id"]:
        return "VIRHE: ei oikeutta poistaa tätä ideaa"

    ideas.delete_idea(idea_id)
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
        return redirect("/login")
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")

    return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")