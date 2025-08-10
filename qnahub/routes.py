from flask import render_template, request, url_for, redirect, flash
from qnahub.forms import RegistrationForm, LoginForm
from qnahub.models import User, Question, Answer, Vote
from qnahub import app,db
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
    #(future) Allow login for both username and email
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) :
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

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/account")
@login_required
def account():

    return render_template("profile.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
