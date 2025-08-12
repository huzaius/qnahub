import os
import secrets
from PIL import Image
from flask import render_template, request, url_for, redirect, flash
from qnahub.forms import RegistrationForm, LoginForm, UpdateProfileForm
from qnahub.models import User, Question, Answer, Vote
from qnahub import app, db
from qnahub import bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/base")
@login_required
def base():
    return render_template("base.html")


@app.route("/question")
def question():
    return render_template("question.html", title="Question")


@app.route("/login", methods=["GET", "POST"])
def login():
    # (future) Allow login for both username and email
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Welcome back, {form.email.data}!", "info")
            return redirect(next_page or url_for("index"))

        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("login.html", form=form, title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/users")
@login_required
def users():
    return render_template("users.html", title=current_user.username)


@app.route("/subjects")
def subjects():
    return render_template("subjects.html")


@app.route("/unanswered")
def unanswered():
    return render_template("unanswered.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = UpdateProfileForm()

    return render_template("settings.html", form=form)

# reduce picture size, re-filename and save


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_fn)

    output_size = (255, 255)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.picture = picture_file
        if form.fullname.data:
            current_user.fullname = form.fullname.data

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("settings"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fullname.data = current_user.fullname
        picture_file = url_for(
            "static", filename="profile_pics/" + current_user.picture)

    return render_template("profile.html", form=form, picture=picture_file)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
