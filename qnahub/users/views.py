from random import shuffle
from datetime import datetime, timezone
import bcrypt
from qnahub import bcrypt, db
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from qnahub.models import Question, User
from qnahub.users.forms import LoginForm, RegistrationForm, UpdateProfileForm
from qnahub.users.utils import save_picture, time_diff


users = Blueprint("users", __name__)


colors= ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']



@users.route("/login", methods=["GET", "POST"])
def login():
    # (future) Allow login for both username and email
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Welcome back, {form.email.data}!", "info")
            return redirect(next_page or url_for("main.index"))

        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("login.html", form=form, title="Login")


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in", "success")
        return redirect(url_for("main.index"))
    return render_template("register.html", form=form)


@users.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = UpdateProfileForm()

    return render_template("settings.html", form=form)


@users.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("users.settings"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fullname.data = current_user.fullname

    picture_file = url_for(
        "static", filename="profile_pics/" + current_user.picture)
    return render_template("profile.html", form=form, picture=picture_file)

@users.route("/users")
def all_users():
    all_users = User.query.all()
   
    return render_template("all_users.html",users=all_users)



@users.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'danger')
    return redirect(url_for('users.all_users'))



@users.route("/user_posts/<string:username>")
@login_required
def user_question(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    questions = Question.query.filter_by(author=user)\
        .order_by( Question.date_posted.desc())\
        .paginate(page=page, per_page=5)
    # Create a copy of the colors list and shuffle it
    shuffled_colors = colors[:]
    shuffle(shuffled_colors)
    return render_template("index.html", questions=questions, colors=shuffled_colors,legend=f'{username}\'s Questions',username=username,page=page,title='User Posts')
   



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))