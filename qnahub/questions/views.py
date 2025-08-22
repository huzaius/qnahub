from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qnahub import db
from qnahub.models import Question
from qnahub.questions.forms import AskQuestionForm

questions = Blueprint("questions", __name__)




@questions.route("/question/<int:question_id>")
def question(question_id):
    question = Question.query.get_or_404(question_id)
    question.views += 1
    db.session.commit()
    return render_template("question.html", question=question)

@questions.route("/question/new", methods=["GET", "POST"])
def new_question():
    form = AskQuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(question)
        db.session.commit()
        flash("Your question has been posted!", "success")
        return redirect(url_for("main.index"))
    return render_template("new_question.html", form=form,legend="Ask a Question")


@questions.route("/edit_question/<int:question_id>", methods=["GET", "POST"])
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
        return redirect(url_for("questions.question", question_id=question.id))  
    elif request.method == "GET":
        form.title.data = question.title
        form.body.data = question.body
    return render_template("new_question.html", form=form, legend="Edit Question")

@questions.route("/delete_question/<int:question_id>", methods=["POST"])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.author != current_user:
        abort(403)
    db.session.delete(question)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('questions.question', question_id=question.id))


@questions.route("/subjects")
def subjects():
    return render_template("subjects.html")