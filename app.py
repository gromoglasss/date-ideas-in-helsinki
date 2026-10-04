import math
import os
import secrets
import sqlite3
from flask import Flask, abort, flash, redirect, render_template, request, session
import markupsafe
import config
import db
import ideas
import users

app = Flask(__name__)
app.secret_key = config.secret_key
app.config["UPLOAD_FOLDER"] = "static/uploads"

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
MAX_PHOTO_SIZE = 2 * 1024 * 1024
PAGE_SIZE = 10

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
# create the tables and add example data if the database is empty
db.init_db()
db.seed_example_data()


@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br>")
    return markupsafe.Markup(content)


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)


def check_idea_form(title, description):
    if not title.strip() or len(title) > 100:
        flash("VIRHE: otsikon pituus on 1-100 merkkiä")
        return False
    if len(description) > 1000:
        flash("VIRHE: kuvaus saa olla enintään 1000 merkkiä")
        return False
    return True


def get_selected_classes():
    all_classes = ideas.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if not entry:
            continue
        parts = entry.split(":")
        if len(parts) != 2:
            abort(403)
        class_title, class_value = parts
        if class_title not in all_classes:
            abort(403)
        if class_value not in all_classes[class_title]:
            abort(403)
        classes.append((class_title, class_value))
    return classes


def save_photo(file):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        flash("VIRHE: kuvan pitää olla jpg, png, gif tai webp")
        return None

    data = file.read()
    if len(data) > MAX_PHOTO_SIZE:
        flash("VIRHE: kuva on liian suuri (enintään 2 Mt)")
        return None

    # random name so that uploads can't overwrite each other
    filename = secrets.token_hex(16) + extension
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    with open(filepath, "wb") as f:
        f.write(data)
    return filename


@app.route("/")
def index():
    query = request.args.get("q", "")
    page = request.args.get("page", "1")
    if not page.isdigit() or int(page) < 1:
        page = "1"
    page = int(page)

    idea_count = ideas.count_ideas(query)
    page_count = max(math.ceil(idea_count / PAGE_SIZE), 1)
    page = min(page, page_count)

    page_ideas = ideas.get_ideas(query, page, PAGE_SIZE)
    return render_template("index.html", ideas=page_ideas, q=query,
                           page=page, page_count=page_count)


@app.route("/idea/<int:idea_id>")
def show_idea(idea_id):
    idea = ideas.get_idea(idea_id)
    if not idea:
        abort(404)

    classes = ideas.get_classes(idea_id)
    comments = ideas.get_comments(idea_id)
    return render_template("ideaTemplate.html", idea=idea, classes=classes,
                           comments=comments)


@app.route("/comment/<int:idea_id>", methods=["POST"])
def add_comment(idea_id):
    if "user_id" not in session:
        return redirect("/login")
    check_csrf()

    idea = ideas.get_idea(idea_id)
    if not idea:
        abort(404)

    content = request.form["content"]
    if not content.strip() or len(content) > 500:
        flash("VIRHE: kommentin pituus on 1-500 merkkiä")
        return redirect("/idea/" + str(idea_id))

    ideas.add_comment(idea_id, session["user_id"], content)
    return redirect("/idea/" + str(idea_id))


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    user_ideas = users.get_ideas(user_id)
    stats = users.get_stats(user_id)
    return render_template("profile.html", user=user, ideas=user_ideas, stats=stats)


@app.route("/temp")
def show_add_form():
    if "user_id" not in session:
        return redirect("/login")
    classes = ideas.get_all_classes()
    return render_template("addIdea.html", classes=classes)


@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")
    check_csrf()

    title = request.form["title"]
    description = request.form["message"]
    if not check_idea_form(title, description):
        return redirect("/temp")
    classes = get_selected_classes()

    filename = ""
    file = request.files.get("photo")
    if file and file.filename:
        filename = save_photo(file)
        if not filename:
            return redirect("/temp")

    idea_id = ideas.add_idea(title, description, filename, session["user_id"], classes)
    return redirect("/idea/" + str(idea_id))


@app.route("/edit/<int:idea_id>", methods=["GET", "POST"])
def edit_idea(idea_id):
    if "user_id" not in session:
        return redirect("/login")

    idea = ideas.get_idea(idea_id)
    if not idea:
        abort(404)

    if idea["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        all_classes = ideas.get_all_classes()
        selected = {}
        for entry in ideas.get_classes(idea_id):
            selected[entry["title"]] = entry["value"]
        return render_template("editIdea.html", idea=idea,
                               all_classes=all_classes, selected=selected)

    check_csrf()
    title = request.form["title"]
    description = request.form["message"]
    if not check_idea_form(title, description):
        return redirect("/edit/" + str(idea_id))
    classes = get_selected_classes()

    ideas.update_idea(idea_id, title, description, classes)
    return redirect("/idea/" + str(idea_id))


@app.route("/delete/<int:idea_id>", methods=["POST"])
def delete_idea(idea_id):
    if "user_id" not in session:
        return redirect("/login")

    idea = ideas.get_idea(idea_id)
    if not idea:
        abort(404)

    if idea["user_id"] != session["user_id"]:
        abort(403)

    check_csrf()
    ideas.delete_idea(idea_id)
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username.strip() or len(username) > 20:
        flash("VIRHE: tunnuksen pituus on 1-20 merkkiä")
        return redirect("/register")

    if not password1:
        flash("VIRHE: salasana ei voi olla tyhjä")
        return redirect("/register")

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu, voit nyt kirjautua sisään")
    return redirect("/login")


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
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    flash("VIRHE: väärä tunnus tai salasana")
    return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
