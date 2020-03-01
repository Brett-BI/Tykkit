from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
bcrypt = Bcrypt()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)

    from .ticket import ticket_routes
    app.register_blueprint(ticket_routes.ticket_bp)

    from .registration import registration_routes
    app.register_blueprint(registration_routes.registration_bp)

    from .auth import auth_routes
    app.register_blueprint(auth_routes.auth_bp)

    return app


from application import models

