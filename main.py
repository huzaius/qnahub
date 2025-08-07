from flask import Flask, render_template, request, url_for, redirect, flash
from forms import RegistrationForm, LoginForm

from flask_sqlalchemy import SQLAlchemy

from models import Answer, Question, Tag, User, Vote

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "d0989a71c8bc68180074af7cb178dac462c617822df3e611865c2429e3a899a050207befcda6862c01a01a742f6a762ce6bc44677d6260c166895eb424c697473529a5b2ce294a9ae8df928b6947204ae6ebabb104d4dbc9ae2385b59c235e6d785bc7aa6cdd54cd3b1022ded52183750095c3dccf2f6113723c6ca45f62432e"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


@app.route("/")
@app.route("/index")
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



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
