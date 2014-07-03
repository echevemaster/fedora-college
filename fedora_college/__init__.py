#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path[0:0] = [""]
from flask import Flask
from flask.ext.babel import Babel
from flask import request
from fedora_college import metadata
from fedora_college.core.constructor import (build_app as build_fedora,
                                             authenticated,
                                             logger, is_admin)


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright


LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}


def build_app(app):
    build_fedora(app)
    authenticated()
    logger(app)
    is_admin(app)
    return app


apps = Flask(__name__)
babel = Babel(apps)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@apps.context_processor
def inject_variables():
    user_admin = is_admin(app)

    return dict(
        is_admin=user_admin)


app = build_app(apps)
if __name__ == '__main__':
    app.run()
