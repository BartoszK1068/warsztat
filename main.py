from flask import Flask, render_template, request, session
from data import db_ops


app = Flask(__name__, template_folder="pages", static_folder="pages")
app.secret_key = "change-me"  # required for session handling


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    user = session.get("user")

    if request.method == "POST":
        login_value = (request.form.get("login") or "").strip()
        password = request.form.get("password") or ""
        message = db_ops.login_user(login_value, password)
        if message == "Zalogowano pomyślnie.":
            session["user"] = login_value
            user = login_value
    elif user:
        message = f"Jesteś zalogowany jako {user}."

    return render_template("login.html", message=message)


@app.route("/register", methods=["POST"])
def register():
    login_value = (request.form.get("login") or "").strip()
    password = request.form.get("password") or ""
    message = db_ops.register_user(login_value, password)
    return render_template("login.html", message=message)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return render_template("login.html", message="Wylogowano.")


if __name__ == "__main__":
    app.run(debug=True)
