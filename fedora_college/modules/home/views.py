#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
bundle = Blueprint('home', __name__, template_folder='templates')


@bundle.route('/', methods=['GET', 'POST'])
@bundle.route('/index/', methods=['GET', 'POST'])
@bundle.route('/home/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html',
                           title='Home', content="Home page")


'''
@bundle.route('/screencasts/',  methods=['GET', 'POST'])
def screencasts():
    return render_template('home/index.html', title='Screen Casts',
                           content="Fedora Screencasts")


@bundle.route('/addmore/', methods=['GET', 'POST'])
def addmore():
    return render_template('home/upload.html', title='Add New Content',
                           content="Upload form & and associated description")
'''


@bundle.route('/about', methods=['GET', 'POST'])
@bundle.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('home/index.html',
                           title='About',
                           content='About Us')
