#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
from fedora_college import db
app = flask.Flask(__name__)
db.init_app(app)

with app.test_request_context():
    db.drop_all()
    db.create_all()
