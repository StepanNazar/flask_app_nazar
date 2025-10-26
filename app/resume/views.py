from flask import render_template
from . import resume_bp


@resume_bp.route("/resume")
def resume() -> str:
    return render_template("resume.html", title="Resume")


@resume_bp.route("/contact")
def contact() -> str:
    return render_template("contact.html", title="Contact")