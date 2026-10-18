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
ERROR_MESSAGES = {
    400: "Lomakkeen tiedot olivat virheelliset.",
    403: "Sinulla ei ole oikeutta tähän toimintoon.",
    404: "Etsimääsi sivua ei löytynyt.",
    405: "Tätä toimintoa ei voi tehdä tällä tavalla.",
}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
# create the tables and add the classes if the database is new
db.init_db()


@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br>")
    return markupsafe.Markup(content)


@app.errorhandler(400)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def show_error(error):
    message = ERROR_MESSAGES[error.code]
    return render_template("error.html", code=error.code, message=message), error.code


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)


def flash_errors(errors):
    for error in errors:
        flash(error, "error")


def check_idea_form(title, description):
    errors = []
    if not title.strip() or len(title) > 100:
        errors.append("VIRHE: otsikon pituus on 1-100 merkkiä")
    if len(description) > 1000:
        errors.append("VIRHE: kuvaus saa olla enintään 1000 merkkiä")
    return errors


def check_photo(extension, data):
    errors = []
    if extension not in ALLOWED_EXTENSIONS:
        errors.append("VIRHE: kuvan pitää olla jpg, png, gif tai webp")
    if len(data) > MAX_PHOTO_SIZE:
        errors.append("VIRHE: kuva on liian suuri (enintään 2 Mt)")
    return errors


def get_selected_classes(all_classes):
    valid_ids = []
    for options in all_classes.values():
        for option in options:
            valid_ids.append(str(option["id"]))

    class_ids = []
    for class_id in request.form.getlist("classes"):
        if class_id not in valid_ids:
            abort(403)
        if int(class_id) not in class_ids:
            class_ids.append(int(class_id))
    return class_ids


def save_photo(extension, data):
    # random name so that uploads can't overwrite each other
    filename = secrets.token_hex(16) + extension
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    with open(path, "wb") as file:
        file.write(data)
    return filename


def render_idea_page(idea, comment):
    classes = ideas.get_classes(idea["id"])
    comments = ideas.get_comments(idea["id"])
    return render_template("ideaTemplate.html", idea=idea, classes=classes,
                           comments=comments, comment=comment)


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
    return render_idea_page(idea, "")


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
        flash("VIRHE: kommentin pituus on 1-500 merkkiä", "error")
        return render_idea_page(idea, content)

    ideas.add_comment(idea_id, session["user_id"], content)
    flash("Kommentti lisätty")
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
    all_classes = ideas.get_all_classes()
    return render_template("addIdea.html", all_classes=all_classes,
                           filled={}, selected=[])


@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")
    check_csrf()

    all_classes = ideas.get_all_classes()
    title = request.form["title"]
    description = request.form["message"]
    class_ids = get_selected_classes(all_classes)
    errors = check_idea_form(title, description)

    extension = ""
    photo_data = b""
    photo = request.files.get("photo")
    if photo and photo.filename:
        extension = os.path.splitext(photo.filename)[1].lower()
        photo_data = photo.read()
        errors += check_photo(extension, photo_data)

    if errors:
        flash_errors(errors)
        if extension:
            flash("Huom: valitse kuva uudelleen ennen lähettämistä", "error")
        filled = {"title": title, "description": description}
        return render_template("addIdea.html", all_classes=all_classes,
                               filled=filled, selected=class_ids)

    filename = ""
    if extension:
        filename = save_photo(extension, photo_data)

    idea_id = ideas.add_idea(title, description, filename, session["user_id"], class_ids)
    flash("Idea lisätty")
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

    all_classes = ideas.get_all_classes()

    if request.method == "GET":
        filled = {"title": idea["title"], "description": idea["description"]}
        selected = ideas.get_class_ids(idea_id)
        return render_template("editIdea.html", idea=idea, all_classes=all_classes,
                               filled=filled, selected=selected)

    check_csrf()
    title = request.form["title"]
    description = request.form["message"]
    class_ids = get_selected_classes(all_classes)

    errors = check_idea_form(title, description)
    if errors:
        flash_errors(errors)
        filled = {"title": title, "description": description}
        return render_template("editIdea.html", idea=idea, all_classes=all_classes,
                               filled=filled, selected=class_ids)

    ideas.update_idea(idea_id, title, description, class_ids)
    flash("Muutokset tallennettu")
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
    flash("Idea poistettu")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    errors = []
    if not username.strip() or len(username) > 20:
        errors.append("VIRHE: tunnuksen pituus on 1-20 merkkiä")
    elif users.username_taken(username):
        errors.append("VIRHE: tunnus on jo varattu")
    if not password1:
        errors.append("VIRHE: salasana ei voi olla tyhjä")
    if password1 != password2:
        errors.append("VIRHE: salasanat eivät ole samat")

    if not errors:
        try:
            users.create_user(username, password1)
            flash("Tunnus luotu, voit nyt kirjautua sisään")
            return redirect("/login")
        except sqlite3.IntegrityError:
            errors.append("VIRHE: tunnus on jo varattu")

    flash_errors(errors)
    return render_template("register.html", filled={"username": username})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={})

    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    flash("VIRHE: väärä tunnus tai salasana", "error")
    return render_template("login.html", filled={"username": username})


@app.route("/logout")
def logout():
    session.clear()
    flash("Olet kirjautunut ulos")
    return redirect("/")
