from flask import redirect, url_for, Blueprint


root_bp = Blueprint(
    "root path", __name__, template_folder="templates", static_folder="static"
)
@root_bp.route("/")
def resume():
    return redirect(url_for("resume.resume"))
