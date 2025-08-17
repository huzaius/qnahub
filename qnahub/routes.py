from datetime import datetime, timezone
import os
from random import randint,shuffle
import secrets
from PIL import Image
from flask import render_template, request, url_for, redirect, flash, abort
from qnahub.forms import RegistrationForm, LoginForm, UpdateProfileForm,AskQuestionForm
from qnahub.models import User, Question, Answer, Vote
from qnahub import app, db
from qnahub import bcrypt
from flask_login import login_user, current_user, logout_user, login_required

colors= ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']

def time_diff(end_time, start_time):
    time_diff = end_time - start_time
    if time_diff.days > 0:
        return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
    elif time_diff.seconds >= 3600:
        hours = time_diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif time_diff.seconds >= 60:
        minutes = time_diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"
    

@app.context_processor
def utility_processor():
    def time_ago(start_time):
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        return time_diff(datetime.now(timezone.utc), start_time)
    return dict(time_ago=time_ago)

@app.route("/index")
@app.route("/")
def index():
    questions = Question.query.order_by(Question.date_posted.desc()).all()
    # Create a copy of the colors list and shuffle it
    shuffled_colors = colors[:]
    shuffle(shuffled_colors)
    return render_template("index.html", questions=questions, colors=shuffled_colors)

@app.route("/base")
@login_required
def base():
    return render_template("base.html")


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



@app.route("/question/<int:question_id>")
def question(question_id):
    question = Question.query.get_or_404(question_id)
    question.views += 1
    db.session.commit()
    return render_template("question.html", question=question)

@app.route("/question/new", methods=["GET", "POST"])
def new_question():
    form = AskQuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(question)
        db.session.commit()
        flash("Your question has been posted!", "success")
        return redirect(url_for("index"))
    return render_template("new_question.html", form=form,legend="Ask a Question")


@app.route("/edit_question/<int:question_id>", methods=["GET", "POST"])
@login_required
def edit_question(question_id):
    
    question = Question.query.get_or_404(question_id)
    if question.author != current_user:
        abort(403)
    
    form = AskQuestionForm()
    if form.validate_on_submit():
        question.title = form.title.data
        question.body = form.body.data 
        db.session.commit()
        flash("Your question has been updated!", "success")
        return redirect(url_for("question", question_id=question.id))
    
    elif request.method == "GET":
        form.title.data = question.title
        form.body.data = question.body


    return render_template("new_question.html", form=form, legend="Edit Question")

@app.route("/delete_question/<int:question_id>", methods=["POST"])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.author != current_user:
        abort(403)
    db.session.delete(question)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('index'))

@app.route("/add_answer/<int:question_id>", methods=["POST"])
def add_answer(question_id):
    question = Question.query.get_or_404(question_id)
    answer_body = request.form.get("answer_body")
    if answer_body:
        answer = Answer(body=answer_body, question=question, author=current_user)
        # db.session.add(answer)
        # db.session.commit()
        flash("Your answer has been posted!", "success")
    return redirect(url_for("question", question_id=question_id))

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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
