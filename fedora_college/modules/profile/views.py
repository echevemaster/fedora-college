#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request, flash, url_for , g , jsonify
from jinja2 import TemplateNotFound
from fedora_college.core.database import db
from fedora_college.modules.profile.forms import *  # noqa
from fedora_college.core.models import *  # noqa
from flask.ext.babel import gettext
from flask_fas_openid import fas_login_required


bundle = Blueprint('profile', __name__, template_folder='templates',
                   static_folder='static')

@bundle.route('/user/edit', methods=['GET', 'POST'])
@bundle.route('/user/<nickname>/edit')
@fas_login_required
def editprofile(nickname = None):
    if g.fas_user['username'] == nickname  or request.method == 'POST':

        #return render_template('profile/add.html')
        form = EditProfile()
        form_action = url_for('profile.editprofile')
        if request.method == 'POST' and form.validate():
            if form.username.data == nickname : 
              query = Screencast(form.username.data,
                                 form.email.data,
                                 form.about.data,
                                 form.website.data,
                                 )
              db.session.add(query)
              db.session.commit()
              flash('User Updated created')
              print "added"
            return(url_for('profile.editprofile'))
        return render_template('profile/add.html', form=form,
                               form_action=form_action, title="Update Profile")
    else:
        return "Unauthorised"


@bundle.route('/user/<nickname>')
@fas_login_required
def user(nickname):
    user = UserProfile.query. \
        filter_by(username=nickname).first()
    if user is None:
        return jsonify({gettext('User '): str(nickname) + gettext(' not found.')})
        # return redirect(url_for('home.index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('profile/user.html',
                           user=user,
                           posts=posts)
