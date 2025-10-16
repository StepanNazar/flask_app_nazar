from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/resume")
def resume() -> str:
    return render_template("resume.html", title="Resume")


@app.route("/contact")
def contact() -> str:
    return render_template("contact.html", title="Contact")


if __name__ == "__main__":
    app.run(debug=True)
