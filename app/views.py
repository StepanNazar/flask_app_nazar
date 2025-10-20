from flask import request, redirect, url_for, render_template, abort
from . import app
from .models import product_repo

@app.route("/")
@app.route("/resume")
def resume() -> str:
    return render_template("resume.html", title="Resume")


@app.route("/contact")
def contact() -> str:
    return render_template("contact.html", title="Contact")

@app.route('/hi/')
@app.route("/hi/<string:name>")
def greetings(name: str = "Guest") -> str:
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)
@app.route("/admin")
def admin():
    return redirect(
        url_for("greetings", name="administrator", age=45, _external=True)
    )

@app.route('/products')
def products():
    products = product_repo.get_all()
    return render_template("products.html",
                           products=products)

@app.route('/product/<int:id>')
def detail_post(id):
    if id > 3:
        abort(404)
    product = product_repo.get_by_id(id)
    return render_template("product_details.html",
                           product=product)
