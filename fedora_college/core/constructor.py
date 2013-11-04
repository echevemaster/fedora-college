from flask import current_app
from flask_fas_openid import FAS
# Imports only in development, in production we use Flask_Bundle
# for automatic bundle's register.
from fedora_college.modules.auth import bundle as auth_bundle
from fedora_college.modules.home import bundle as home_bundle
from fedora_college.core.database import db


def build_app(app):
    app.register_blueprint(auth_bundle)
    app.register_blueprint(home_bundle)
    # Config to Flask from objects
    #app.config.from_object('fedora_college.core.ProductionConfig')
    app.config.from_object('fedora_college.core.config.DevelopmentConfig')

    # FAS OpenID Instance
    with app.app_context():
        current_app.config['fas'] = FAS(app)


def create_db(app):
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
