#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template,
                   request, redirect, url_for, g, jsonify)
from fedora_college.core.database import db
from fedora_college.modules.profile.forms import *  # noqa
from fedora_college.core.models import *  # noqa
from flask.ext.babel import gettext
from flask_fas_openid import fas_login_required


bundle = Blueprint('profile', __name__, template_folder='templates',
                   static_folder='static')


@bundle.route('/user/edit/', methods=['GET', 'POST'])
@bundle.route('/user/edit', methods=['GET', 'POST'])
@bundle.route('/user/<nickname>/edit/', methods=['GET', 'POST'])
@bundle.route('/user/<nickname>/edit', methods=['GET', 'POST'])
@fas_login_required
def editprofile(nickname=None):
    if g.fas_user['username'] == nickname or request.method == 'POST':
        user = UserProfile.query. \
            filter_by(username=nickname).first()

        form = EditProfile(obj=user)

        form_action = url_for('profile.editprofile')
        if form.username.data == nickname and request.method == 'POST':
            form.populate_obj(user)
            print user.getdata()
            db.session.commit()
            return redirect(url_for('profile.user',
                            nickname=nickname, updated="True"))
        return render_template('profile/edit_user_profile.html', form=form,
                               form_action=form_action, title="Update Profile")
    else:
        return "Unauthorised"


@bundle.route('/user/<nickname>')
@fas_login_required
def user(nickname):

    msg = ""
    if request.args.get('updated') == "True":
        msg = msg + "Profile Updated"
        print msg
    user = UserProfile.query. \
        filter_by(username=nickname).first()
    if user is None:
        return jsonify({gettext('User'): str(nickname) + gettext('not found.')})

    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('profile/user_profile.html',
                           user=user,
                           posts=posts,
                           url=str(
                               url_for(
                                   'profile.editprofile', nickname=nickname,)),
                           message=msg)
