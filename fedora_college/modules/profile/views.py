# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, render_template
from flask.ext.babel import gettext
from flask_fas_openid import fas_login_required
from fedora_college.core.models import *  # noqa

bundle = Blueprint('profile', __name__, template_folder='templates')


@bundle.route('/user/<nickname>')
@fas_login_required
def user(nickname):
    user = UserProfile.query. \
    filter_by(username=nickname).first()
    if user is None:
        return jsonify({gettext('User '): str(nickname) + gettext(' not found.')})
        # return redirect(url_for('home.index'))
    posts=[
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user = user,
                           posts=posts)
