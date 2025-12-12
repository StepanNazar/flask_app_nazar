from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
)
from flask_login import current_user, login_user, login_required, logout_user

from app import db
from . import users_bp
from .forms import LoginForm, RegistrationForm
from .models import User


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
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            message = f"Login successful! Welcome back, {user.username}!" + (
                " You will be remembered after closing your browser." if remember_me else ""
            )
            flash(message, "success")
            return redirect(url_for("users.account"))

        flash("Incorrect username or password!", "danger")
        return redirect(url_for("users.login"))
    return render_template("login.html", login_form=form)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()

        flash(f"Registration successful! Welcome, {user.username}! You can now log in.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", registration_form=form)

@users_bp.route("/logout")
def logout():
    logout_user()
    flash("Logout successful!", "success")
    return redirect(url_for("users.login"))


@users_bp.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)

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


@users_bp.route("/users")
@login_required
def users_list():
    """Display list of all registered users"""
    all_users = User.query.all()
    users_count = len(all_users)
    return render_template("users_list.html", users=all_users, users_count=users_count)
