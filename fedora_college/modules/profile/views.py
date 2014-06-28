#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, abort,
                   request, redirect, url_for, g, jsonify)
from fedora_college.core.database import db
from sqlalchemy import desc
from fedora_college.modules.profile.forms import *  # noqa
from fedora_college.core.models import *  # noqa


bundle = Blueprint('profile', __name__, template_folder='templates',
                   static_folder='static')


def getuserdata():
    media = Media.query.filter_by(
        user_id=g.fas_user['username']).\
        order_by(desc(Media.timestamp)).limit(10).all()
    comments = Comments.query.filter_by(
        username=g.fas_user['username']).\
        order_by(desc(Comments.date_added)).limit(10).all()
    content = Content.query.filter_by(
        user_id=g.fas_user['username']). \
        order_by(desc(Content.date_added)).limit(10).all()
    return media, content, comments


def authenticated():
    return hasattr(g, 'fas_user') and g.fas_user


@bundle.route('/user/edit/', methods=['GET', 'POST'])
@bundle.route('/user/edit', methods=['GET', 'POST'])
@bundle.route('/user/<nickname>/edit/', methods=['GET', 'POST'])
@bundle.route('/user/<nickname>/edit', methods=['GET', 'POST'])
def editprofile(nickname=None):
    if authenticated():
        if g.fas_user['username'] == nickname or request.method == 'POST':
            user = UserProfile.query. \
                filter_by(username=nickname).first_or_404()

            form = EditProfile(obj=user)
            form_action = url_for('profile.editprofile')
            if form.username.data == nickname and form.validate_on_submit():
                form.populate_obj(user)
                db.session.commit()
                return redirect(url_for('profile.user',
                                nickname=nickname, updated="True"))

            return render_template('profile/edit_user_profile.html',
                                   form=form,
                                   form_action=form_action,
                                   title="Update Profile",
                                   )
        else:
            return "Unauthorised"
    abort(404)


@bundle.route('/user/<nickname>')
def user(nickname):

    msg = ""
    if request.args.get('updated') == "True":
        msg = msg + "Profile Updated"
        print msg
    user = UserProfile.query. \
        filter_by(username=nickname).first()
    if user is None:
        return jsonify({'User': str(nickname) + 'not found.'})

    media, content, comments = getuserdata()
    return render_template('profile/user_profile.html',
                           user=user,
                           medias=media,
                           contents=content,
                           comments=comments,
                           url=str(
                               url_for(
                                   'profile.editprofile', nickname=nickname,)),
                           message=msg,
                           newtoken=url_for('auth.gentoken'))
