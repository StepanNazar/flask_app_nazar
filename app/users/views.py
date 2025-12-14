import os
import secrets
from datetime import datetime, timezone
from PIL import Image
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
    current_app,
)
from flask_login import current_user, login_user, login_required, logout_user

from app import db
from . import users_bp
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm
from .models import User


@users_bp.before_app_request
def before_request():
    """Update last_seen for authenticated users"""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


def save_picture(form_picture):
    """Save uploaded profile picture and create thumbnail"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    profile_pics_path = os.path.join(current_app.root_path, 'static/images/profile_pics')
    thumbnails_path = os.path.join(current_app.root_path, 'static/images/profile_pics/thumbnails')
    os.makedirs(profile_pics_path, exist_ok=True)
    os.makedirs(thumbnails_path, exist_ok=True)
    picture_path = os.path.join(profile_pics_path, picture_fn)
    thumbnail_path = os.path.join(thumbnails_path, picture_fn)

    i = Image.open(form_picture)
    max_size = (400, 400)
    i_original = i.copy()
    i_original.thumbnail(max_size)
    i_original.save(picture_path)
    thumbnail_size = (128, 128)
    i.thumbnail(thumbnail_size)
    i.save(thumbnail_path)

    return picture_fn


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


@users_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='images/profile_pics/' + (current_user.image or 'profile_default.jpg'))
    return render_template("account.html", user=current_user, form=form, image_file=image_file)


@users_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been changed!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Current password is incorrect!', 'danger')
    return render_template("change_password.html", form=form)

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
