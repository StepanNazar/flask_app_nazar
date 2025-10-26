from flask import render_template, request, redirect, url_for
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