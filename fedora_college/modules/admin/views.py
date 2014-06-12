#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import TemplateNotFound
from flask import Blueprint, render_template, abort, request, flash, url_for
from fedora_college.core.database import db
from fedora_college.core.forms import AddScreenCast
from fedora_college.core.models import *  # noqa
from flask_fas_openid import fas_login_required, cla_plus_one_required

bundle = Blueprint('admin', __name__, template_folder='templates',
                   static_folder='static')


@bundle.route('/admin', methods=['GET', 'POST'])
@fas_login_required
@cla_plus_one_required
def index():
    try:
        return render_template('admin/index.html')
    except TemplateNotFound:
        abort(404)


@bundle.route('/admin/screencasts', methods=['GET', 'POST'])
@fas_login_required
@cla_plus_one_required
def screencast():
    sc = Screencast.query.all()
    print sc
    return render_template('admin/screencast.html')


@bundle.route('/admin/screencasts/add', methods=['GET', 'POST'])
@fas_login_required
@cla_plus_one_required
def add_screencast():
    form = AddScreenCast()
    form_action = url_for('admin.add_screencast')
    if request.method == 'POST' and form.validate():
        screencast_file = request.files['url_video']
        query = Screencast(form.title.data,
                           form.slug.data,
                           form.description.data,
                           form.date.data,
                           screencast_file,
                           form.date.active
                           )
        db.session.add(query)
        db.session.commit()
        flash('Screencast created')
        return(url_for('admin.screencast'))
    return render_template('admin/add_screencast.html', form=form,
                           form_action=form_action, title="Add Screencast")
