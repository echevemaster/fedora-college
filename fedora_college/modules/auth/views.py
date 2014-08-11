# -*- coding: utf-8 -*-
from flask import request, Blueprint, redirect
from flask import url_for, g, current_app
from flask import jsonify
from flask_fas_openid import fas_login_required
from fedora_college.core.models import *  # noqa
from fedora_college.core.database import db


bundle = Blueprint('auth', __name__, url_prefix='/auth')

'''
Send email on user registration
'''


def send_email(sender, recipients, subject, body, html):
    msg = Message(subject, sender)
    msg = mail.send(msg)
    return str(msg)

'''
Handler for the login
'''


@bundle.route('/login', methods=['GET', 'POST'])
def auth_login():
    if 'next' in request.args:
        next_url = request.args['next']
    else:
        next_url = url_for('home.index')
    next_url = url_for('auth.after_auth')
    if g.fas_user:
        return redirect(next_url)
    return current_app.config['fas'].login(return_url=next_url)

'''
Handler for the logout
'''


@bundle.route('/logout', methods=['GET', 'POST'])
def auth_logout():
    if g.fas_user:
        current_app.config['fas'].logout()
    return redirect(url_for('home.index'))

'''
Testing Handler
'''


@bundle.route('/test/media', methods=['GET', 'POST'])
@fas_login_required
def testMedia():
    try:
        media = Media.query. \
            filter_by(user_id=g.fas_user['username']).first()
        return jsonify(media.getdata())
    except Exception:
        return "None"

'''
    Testing user login
'''


@bundle.route('/test', methods=['GET', 'POST'])
@fas_login_required
def testProfile():
    try:
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first()
        return jsonify(user.getdata())
    except:
        return "None"

'''
Insert into database
'''


@bundle.route('/insert', methods=['GET', 'POST'])
@fas_login_required
def after_auth():
    try:
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first()
        if user is None:
            raise Exception("User is not in database ")
        return redirect(url_for('profile.user',
                        nickname=g.fas_user['username'])
                        )

    except Exception:
        groups = g.fas_user['groups']
        if len(groups) > 0:
            user_type = "author"
        else:
            user_type = "user"

        user = UserProfile(
            str(g.fas_user['username']),
            str(g.fas_user['username']),
            str(g.fas_user['email']),
            " ", " ", user_type)
        try:
            sender = "fedoracollege@engineerinme.com"
            subject = "Welcome to Fedora Virtual Classroom"
            body = "On Behalf of fedora COmmunity I welcome you."
            html = "Welcome to world of learning "
            send_email(sender, g.fas_user['email'], subject, body, html)
        except Exception:
            pass
        user.newtoken()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profile.editprofile',
                                nickname=g.fas_user['username'])
                        )

'''
Renew /Get a authentication
access token for api
'''


@bundle.route('/gettoken', methods=['GET', 'POST'])
@fas_login_required
def gentoken():
    user = UserProfile.query. \
        filter_by(username=g.fas_user['username']).first()
    user.newtoken()
    db.session.commit()
    return redirect(url_for('profile.user', nickname=g.fas_user['username']))
