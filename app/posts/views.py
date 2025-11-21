from flask import session, redirect, url_for, flash, render_template

from . import post_bp
from .forms import PostForm, DeletePostForm
from .models import Post
from app import db


@post_bp.route("/")
def all_posts():
    posts = db.session.query(Post).order_by(Post.posted.desc()).all()
    return render_template("all_posts.html", posts=posts)

@post_bp.route("/create", methods=["GET", "POST"])
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=session.get("username", "Anonymous"),
            posted=form.posted.data,
            is_active=form.is_active.data,
        )
        db.session.add(post)
        db.session.commit()
        flash(f"Post '{post.title}' has been added!", "success")
        return redirect(url_for("posts.read", id=post.id))
    elif form.errors != {}:
        flash("There were some errors in your form. Please correct them and try again.", "danger")
    return render_template("create_post.html", create_form=form)

@post_bp.route("/read/<int:id>")
def read(id):
    post = db.session.get(Post, id)
    if post is None:
        flash(f"Post with id {id} not found.", "danger")
        return redirect(url_for("posts.all_posts"))
    return render_template("read_post.html", post=post)

@post_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    post = db.session.get(Post, id)
    if post is None:
        flash(f"Post with id {id} not found.", "danger")
        return redirect(url_for("posts.all_posts"))
    form = PostForm(obj=post)
    # Remove validators from fields that should not be edited
    del form.author_id
    del form.posted
    if not form.is_submitted():
        form.category.data = post.category.value
        form.is_active.data = post.is_active
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        db.session.commit()
        flash(f"Post '{post.title}' has been edited!", "success")
        return redirect(url_for("posts.read", id=post.id))
    return render_template("edit_post.html", form=form)

@post_bp.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    post = db.session.get(Post, id)
    if post is None:
        flash(f"Post with id {id} not found.", "danger")
        return redirect(url_for("posts.all_posts"))
    form = DeletePostForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash(f"Post '{post.title}' has been deleted!", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("delete_post.html", post=post, delete_form=form)