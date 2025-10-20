from flask import render_template, abort
from .models import product_repo
from . import products_bp


@products_bp.route('/')
def products():
    products = product_repo.get_all()
    return render_template("products.html",
                           products=products)

@products_bp.route('/<int:id>')
def detail_post(id):
    if id > 3:
        abort(404)
    product = product_repo.get_by_id(id)
    return render_template("product_details.html",
                           product=product)