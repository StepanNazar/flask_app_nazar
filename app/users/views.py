from flask import render_template, request, redirect, url_for, flash, session
from . import users_bp


@users_bp.route('/hi/')
@users_bp.route("/hi/<string:name>")
def greetings(name: str = "Guest") -> str:
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)
@users_bp.route("/admin")
def admin():
    return redirect(
        url_for("users.greetings", name="administrator", age=45, _external=True)
    )

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = [("admin", "admin"), ("user1", "password")]
        username = request.form.get("username")
        password = request.form.get("password")
        if (username, password) in users:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("users.profile"))
        flash("Incorrect username or password!", "danger")
    return render_template("login.html")

@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logout successful!", "success")
    return redirect(url_for("users.login"))

@users_bp.route("/profile")
def profile():
    if "username" in session:
        return render_template("profile.html", username=session["username"])
    flash("Please login first!", "danger")
    return redirect(url_for("users.login"))