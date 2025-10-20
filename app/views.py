from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route("/")
@app.route("/resume")
def resume() -> str:
    return render_template("resume.html", title="Resume")


@app.route("/contact")
def contact() -> str:
    return render_template("contact.html", title="Contact")
