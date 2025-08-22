from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qnahub import db
from qnahub.models import Answer, Question
from qnahub.questions.forms import AskQuestionForm




answers = Blueprint("answers", __name__)


@answers.route("/add_answer/<int:question_id>", methods=["POST"])
def add_answer(question_id):
    question = Question.query.get_or_404(question_id)
    answer_body = request.form.get("answer_body")
    if answer_body:
        answer = Answer(body=answer_body, question=question, author=current_user)
        db.session.add(answer)
        db.session.commit()
        flash("Your answer has been posted!", "success")
    return redirect(url_for("questions.question", question_id=question_id))

@answers.route("/delete_answer/<int:answer_id>", methods=["POST"])
@login_required
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if answer.author != current_user:
        abort(403)
    db.session.delete(answer)
    db.session.commit()
    flash('Your answer has been deleted!', 'success')
    return redirect(url_for('questions.question', question_id=answer.question_id))

@answers.route("/edit_answer/<int:answer_id>", methods=["GET", "POST"])
@login_required
def edit_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if answer.author != current_user:
        abort(403)
    form = AskQuestionForm()
    if form.validate_on_submit():
        answer.body = form.body.data
        db.session.commit()
        flash("Your answer has been updated!", "success")
        return redirect(url_for("questions.question", question_id=answer.question.id))
    elif request.method == "GET":
        form.body.data = answer.body
    return render_template("new_question.html", form=form, legend="Edit Answer")



@answers.route("/unanswered")
def unanswered():
    return render_template("unanswered.html")


