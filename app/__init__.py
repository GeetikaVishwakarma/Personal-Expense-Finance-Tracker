from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config


db = SQLAlchemy()

login_manager = LoginManager()

csrf = CSRFProtect()


login_manager.login_view = "auth.login"

login_manager.login_message_category = "warning"


def create_app(config_class=Config):

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    app.config.from_object(config_class)

    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True
    )

    db.init_app(app)

    login_manager.init_app(app)

    csrf.init_app(app)


    from app.auth import auth_bp
    from app.main import main_bp


    app.register_blueprint(auth_bp)

    app.register_blueprint(main_bp)


    with app.app_context():

        db.create_all()


    return app