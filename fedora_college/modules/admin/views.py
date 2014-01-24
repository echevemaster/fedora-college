#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request, \
    redirect, flash, url_for
from jinja2 import TemplateNotFound
from fedora_college.core.forms import AddScreenCast
bundle = Blueprint('admin', __name__, template_folder='templates',
                   static_folder='static')


@bundle.route('/admin', methods=['GET', 'POST'])
def index():
    try:
        return render_template('admin/index.html')
    except TemplateNotFound:
        abort(404)


@bundle.route('/admin/screencasts', methods=['GET', 'POST'])
def screencast():
    return render_template('admin/screencast.html')


@bundle.route('/admin/screencasts/add', methods=['GET', 'POST'])
def add_screencast():
    form = AddScreenCast()
    form_action = url_for('admin.add_screencast')
    return render_template('admin/add_screencast.html',
                           form=form,
                           form_action=form_action,
                           title="Add Screencast")
