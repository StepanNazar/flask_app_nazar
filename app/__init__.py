import logging
import os
from logging.handlers import RotatingFileHandler

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

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240,
                                   backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask app started')