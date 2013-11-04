#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":mod:`fedora_college.main` -- Program entry point
"""
import sys
sys.path[0:0] = [""]

import flask
from flask.ext.script import Manager
from fedora_college.core.constructor import (build_app as build_fedora,
                                             create_db)


app = flask.Flask(__name__)
manager = Manager(app)


def build_app():
    build_fedora(app)


@manager.command
def create_database():
    create_db(app)


@manager.command
def run():
    app.run(debug=True)

if __name__ == '__main__':
    build_app()
    manager.run()
