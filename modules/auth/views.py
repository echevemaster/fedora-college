#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (request, Blueprint, url_for, redirect, g, current_app)
from flask_fas_openid import fas_login_required

bundle = Blueprint('auth', __name__, url_prefix='/auth')


@bundle.route('/login', methods=['GET', 'POST'])
def auth_login():
    if 'next' in request.args:
        next_url = request.args['next']
    else:
        next_url = url_for('home.index')
    if g.fas_user:
        return redirect(next_url)
    return current_app.config['fas'].login(return_url=next_url)


@bundle.route('/logout', methods=['GET', 'POST'])
def auth_logout():
    if g.fas_user:
        current_app.config['fas'].logout()
    return redirect(url_for('home.index'))


@bundle.route('/test', methods=['GET', 'POST'])
@fas_login_required
def auth_test():
    return 'FAS OK'
