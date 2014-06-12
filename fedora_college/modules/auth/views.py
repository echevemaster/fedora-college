# -*- coding: utf-8 -*-
from flask import request, Blueprint, redirect
from flask import url_for, g, current_app
from flask import jsonify
from flask_fas_openid import fas_login_required
from fedora_college.core.models import *  # noqa

bundle = Blueprint('auth', __name__, url_prefix='/auth')


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
        return jsonify(media.getdata())
    except Exception as e:
        print e
        return "None"


@bundle.route('/test', methods=['GET', 'POST'])
@fas_login_required
def testProfile():
    try:
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first()
        return jsonify(user.getdata())
    except:
        return "None"


@bundle.route('/insert', methods=['GET', 'POST'])
@fas_login_required
def after_auth():
    try:
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first()
        print user.getdata()
        #return jsonify(user.getdata())
        return redirect(url_for('profile.user',
                        nickname=g.fas_user['username'])
                        )

    except Exception as e:
        print e
        # return jsonify(g.fas_user)
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
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profile.editprofile',
                                nickname=g.fas_user['username'])
                        )


@bundle.route('/gettoken', methods=['GET', 'POST'])
@fas_login_required
def gentoken():
    user = UserProfile.query. \
        filter_by(username=g.fas_user['username']).first()
    user.newtoken()
    db.session.commit()
    return redirect(url_for('profile.user', nickname=g.fas_user['username']))
