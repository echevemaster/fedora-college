#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (request, Blueprint,
                   url_for, redirect, g, current_app)
from flask_fas_openid import fas_login_required
from fedora_college.core.models import *  # noqa

bundle = Blueprint('auth', __name__, url_prefix='/auth')


@bundle.route('/login', methods=['GET', 'POST'])
def auth_login():
    if 'next' in request.args:
        next_url = request.args['next']
    else:
        next_url = url_for('auth.after_auth')
    if g.fas_user:
        return redirect(next_url)
    return current_app.config['fas'].login(return_url=next_url)


@bundle.route('/logout', methods=['GET', 'POST'])
def auth_logout():
    if g.fas_user:
        current_app.config['fas'].logout()
    return redirect(url_for('home.index'))


@bundle.route('/test/media', methods=['GET', 'POST'])
@fas_login_required
def testMedia():
    try:
        media = Media.query. \
            filter_by(user_id=g.fas_user['username']).first()
        return str(media)
    except:
        return "None"


@bundle.route('/test', methods=['GET', 'POST'])
@fas_login_required
def testProfile():
    try:
        user = UserProfile.query. \
            filter_by(user_id=g.fas_user['username']).first()
        return str(user.getdata())
    except:
        return "None"


@bundle.route('/insert', methods=['GET', 'POST'])
@fas_login_required
def after_auth():
    try:
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first()
        return redirect(url_for('home.index'))
        # return jsonify(user.getdata())

    except Exception as e:
        print e

        user = UserProfile(
            str(g.fas_user['username']),
            str(g.fas_user['username']),
            str(g.fas_user['email']),
            "Testing", "xyz.com", "user")
        db.session.add(user)
        db.session.commit()
        print str(g.fas_user) + "FAS OK"
        return redirect(url_for('home.index'))
        # return str(g.fas_user) + "FAS OK"
