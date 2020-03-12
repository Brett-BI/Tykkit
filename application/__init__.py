from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
bcrypt = Bcrypt()
bootstrap = Bootstrap()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        #db.create_all()

        from .ticket import ticket_routes
        app.register_blueprint(ticket_routes.ticket_bp)

        from .registration import registration_routes
        app.register_blueprint(registration_routes.registration_bp)

        from .auth import auth_routes
        app.register_blueprint(auth_routes.auth_bp)

        from .main import main_routes
        app.register_blueprint(main_routes.main_bp)

        from . import filters
        app.register_blueprint(filters.filters)

        return app

