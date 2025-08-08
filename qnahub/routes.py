from flask import render_template, request, url_for, redirect, flash
from qnahub.forms import RegistrationForm, LoginForm

from qnahub import app





@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/question")
def question():
    return render_template("question.html", title="Question")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "huzaius@gmail.com" and form.password.data == "password":
            flash(f"Account Login Successfully for {form.email.data}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("login.html", form=form, title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/users")
def users():
    return render_template("users.html")


@app.route("/subjects")
def subjects():
    return render_template("subjects.html")


@app.route("/unanswered")
def unanswered():
    return render_template("unanswered.html")
