from flask import Flask,render_template,request,url_for,redirect,flash




app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/users")
def users():
    return render_template("users.html")

@app.route("/dashboard")
def dasboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)

