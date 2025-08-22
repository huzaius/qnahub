from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "d0989a71c8bc68180074af7cb178dac462c617822df3e611865c2429e3a899a050207befcda6862c01a01a742f6a762ce6bc44677d6260c166895eb424c697473529a5b2ce294a9ae8df928b6947204ae6ebabb104d4dbc9ae2385b59c235e6d785bc7aa6cdd54cd3b1022ded52183750095c3dccf2f6113723c6ca45f62432e"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["UPLOAD_FOLDER"] = "static/profile_pics"
app.config["ALLOWED_EXTENSIONS"] = ["jpg", "png"]

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from qnahub.main.views import main
from qnahub.questions.views import questions
from qnahub.answers.views import answers
from qnahub.users.views import users

app.register_blueprint(main)
app.register_blueprint(questions)
app.register_blueprint(answers)
app.register_blueprint(users)