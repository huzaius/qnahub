from random import shuffle
from flask import Blueprint, render_template, request
from qnahub.models import Question




main = Blueprint("main", __name__)


colors= ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']


@main.route("/index")
@main.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    questions = Question.query.order_by(Question.date_posted.desc()).paginate(page=page, per_page=5)
    # Create a copy of the colors list and shuffle it
    shuffled_colors = colors[:]
    shuffle(shuffled_colors)
    return render_template("index.html", questions=questions, colors=shuffled_colors,legend="All Questions",title="Q&A Hub - Home")
