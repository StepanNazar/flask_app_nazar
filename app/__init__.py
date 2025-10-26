from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("config.py")

from . import views
from .users import users_bp
from .resume import resume_bp
from .products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(products_bp)