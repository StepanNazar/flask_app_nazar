from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
)
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
        color_scheme = request.cookies.get("color_scheme", "light")
        response = make_response(
            render_template("profile.html", username=session["username"], color_scheme=color_scheme)
        )
        response.set_cookie("color_scheme", color_scheme, max_age=60*60*24*365) # update expiration date
        return response
    flash("Please login first!", "danger")
    return redirect(url_for("users.login"))

@users_bp.route("/set-color-scheme/<scheme>")
def set_color_scheme(scheme):
    if scheme not in ["light", "dark"]:
        flash("Invalid color scheme!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("color_scheme", scheme, max_age=60*60*24*365)
    flash(f"Color scheme changed to {scheme}!", "success")
    return response

@users_bp.route("/add-cookie", methods=["POST"])
def add_cookie():
    cookie_name = request.form.get("cookie_name")
    cookie_value = request.form.get("cookie_value")
    cookie_expires = request.form.get("cookie_expires")
    response = make_response(redirect(url_for("users.profile")))
    if cookie_name and cookie_value and cookie_expires:
        if cookie_name in request.cookies.keys():
            flash(f"Cookie '{cookie_name}' already exists!", "warning")
        else:
            response.set_cookie(cookie_name, cookie_value, max_age=int(cookie_expires))
            flash(f"Cookie '{cookie_name}' added!", "success")
    else:
        flash("Please fill out the form!", "danger")
    return response

@users_bp.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    cookie_name = request.form.get("cookie_name")
    response = make_response(redirect(url_for("users.profile")))
    if cookie_name:
        response.delete_cookie(cookie_name)
        flash(f"Cookie '{cookie_name}' deleted!", "success")
    else:
        flash("Please fill out the form!", "danger")
    return response

@users_bp.route("/delete-cookies", methods=["POST"])
def delete_all_cookies():
    response = make_response(redirect(url_for("users.profile")))
    for cookie_name in request.cookies.keys():
        response.delete_cookie(cookie_name)
    flash("All cookies deleted!", "success")
    return response