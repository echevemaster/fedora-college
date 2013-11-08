#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from fedora_college.core.forms import AddScreenCast
bundle = Blueprint('admin', __name__, template_folder='templates')


@bundle.route('/admin/', methods=['GET', 'POST'])
def index():
    return render_template('admin/index.html')


@bundle.route('/admin/screencasts', methods=['GET', 'POST'])
def screencast():
    return render_template('admin/screencast.html')


@bundle.route('/admin/screencast/add', methods=['GET', 'POST'])
def screencast_add():
    form_screencast = AddScreenCast()
    return render_template('admin/add_screencast.html',
                           form_screencast=form_screencast)
