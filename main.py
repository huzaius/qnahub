from flask import Flask,render_template,request,url_for,redirect,flash
from forms import RegistrationForm,LoginForm



app = Flask(__name__)


@app.route("/")
@app.route("/base")
def base():
    return render_template("base.html")



@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/question")
def question():
    return render_template("question.html",title="Question")

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    return render_template("login.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    return render_template("register.html",form=form)

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
    app.run(debug=True)

