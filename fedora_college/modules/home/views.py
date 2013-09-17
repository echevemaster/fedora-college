#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
bundle = Blueprint('home', __name__, template_folder='templates')


@bundle.route('/', methods=['GET', 'POST'])
@bundle.route('/index', methods=['GET', 'POST'])
@bundle.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')
