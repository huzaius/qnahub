from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "d0989a71c8bc68180074af7cb178dac462c617822df3e611865c2429e3a899a050207befcda6862c01a01a742f6a762ce6bc44677d6260c166895eb424c697473529a5b2ce294a9ae8df928b6947204ae6ebabb104d4dbc9ae2385b59c235e6d785bc7aa6cdd54cd3b1022ded52183750095c3dccf2f6113723c6ca45f62432e"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from qnahub import routes