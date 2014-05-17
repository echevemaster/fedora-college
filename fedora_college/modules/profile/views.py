# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, jsonify, current_app, flash, redirect, url_for, render_template
from werkzeug import secure_filename
from flask.ext.babel import gettext

from fedora_college.core.models import *  # noqa

bundle = Blueprint('profile', __name__, template_folder='templates')


@bundle.route('/user/<nickname>')
#@login_required
def user(nickname):
    user = UserProfile.query.filter_by(username=nickname).first()
    if user is None:
        return jsonify({'User ': str(nickname) + ' not found.'})
        # return redirect(url_for('home.index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)