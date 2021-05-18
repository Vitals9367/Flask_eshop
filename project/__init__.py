from flask import Flask, url_for
from .extensions import db, login_manager, whooshee
from .admin import admin
from project.settings import Config
from flask_migrate import Migrate, MigrateCommand


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.app = app

    db.init_app(app)
    whooshee.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    db.create_all()

    from project.auth.routes import auth
    from project.main.routes import main
    from project.profile.routes import profile
    from project.errors.routes import errors

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(profile)
    app.register_blueprint(errors)

    admin.init_app(app)

    return app
