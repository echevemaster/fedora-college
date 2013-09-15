#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from core import build_app
from core.database import db

app = flask.Flask(__name__)
build_app(app)

if __name__ == '__main__':
    app.run(debug=True)
