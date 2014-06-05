#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from fedora_college.core.models import *  # noqa
bundle = Blueprint('home', __name__, template_folder='templates')


@bundle.route('/', methods=['GET', 'POST'])
@bundle.route('/index/', methods=['GET', 'POST'])
@bundle.route('/home/', methods=['GET', 'POST'])
def index():
    posts = Content.query. \
        filter_by(type_content="blog").all()

    screen = Content.query. \
        filter_by(type_content="media").all()

    media = Media.query.all()
    return render_template('home/index.html',
                           title='Home',
                           content="Home page",
                           screen=screen,
                           media=media,
                           posts=posts)


@bundle.route('/about', methods=['GET', 'POST'])
@bundle.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('home/index.html',
                           title='About',
                           content='About Us')


@bundle.route('/feedback', methods=['GET', 'POST'])
@bundle.route('/feedback/', methods=['GET', 'POST'])
def feedback():
    return render_template('home/index.html',
                           title='Feedback',
                           content='Feedback')
