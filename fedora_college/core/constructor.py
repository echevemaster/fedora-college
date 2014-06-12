import logging
from flask import current_app, g
from flask_fas_openid import FAS
# Imports only in development, in production we use Flask_Bundle
# for automatic bundle's register.
from fedora_college.modules.auth import bundle as auth_bundle
from fedora_college.modules.home import bundle as home_bundle
from fedora_college.modules.admin import bundle as admin_bundle
from fedora_college.modules.api import bundle as api_bundle
from fedora_college.modules.profile import bundle as profile_bundle
from fedora_college.modules.content import bundle as content_bundle
from fedora_college.core.database import db


def build_app(app):
    app.register_blueprint(auth_bundle)
    app.register_blueprint(home_bundle)
    app.register_blueprint(admin_bundle)
    app.register_blueprint(api_bundle)
    app.register_blueprint(profile_bundle)
    app.register_blueprint(content_bundle)
    # Config to Flask from objects
    # app.config.from_object('fedora_college.core.ProductionConfig')
    app.config.from_object('fedora_college.core.config.DevelopmentConfig')
    db.init_app(app)

    # FAS OpenID Instance
    with app.app_context():
        current_app.config['fas'] = FAS(app)


def create_db(app):
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()


def drop_db(app):
    db.init_app(app)
    with app.app_context():
        db.drop_all()


def authenticated():
    return hasattr(g, 'fas_user') and g.fas_user


def logger(app):
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setLevel(logging.ERROR)
        app.logger.addHandler(handler)
        LOG = app.logger
        return LOG


def is_admin(app):
    if not authenticated() \
            or not g.fas_user.cla_done \
            or len(g.fas_user.groups) < 1:
        return False

    admins = app.config['ADMIN_GROUP']

    if isinstance(admins, basestring):
        admins = set([admins])
    else:
        admins = set(admins)
    groups = set(g.fas_user.groups)
    return not groups.isdisjoint(admins)
