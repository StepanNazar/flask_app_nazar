from flask import redirect, url_for
from . import app


@app.route("/")
def resume():
    return redirect(url_for("resume.resume"))
