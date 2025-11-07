import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app(config: type[Config]):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import root_bp
    from .users import users_bp
    from .resume import resume_bp
    from .products import products_bp
    from .posts import post_bp

    app.register_blueprint(root_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(post_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

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

    return app