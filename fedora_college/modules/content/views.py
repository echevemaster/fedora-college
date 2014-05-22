#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
bundle = Blueprint('content', __name__, template_folder='templates')


@bundle.route('/blog', methods=['GET', 'POST'])
@bundle.route('/blog/', methods=['GET', 'POST'])
@bundle.route('/blog/<slug>/', methods=['GET', 'POST'])
@bundle.route('/blog/<slug>', methods=['GET', 'POST'])
def blog(slug=None):
    if slug is not None:
        try:
            posts = Content.query. \
                filter_by(type_content="blog").all()
        except:
            posts = "No such posts in database."
    else:

        try:
            posts = Content.query. \
                filter_by(type_content="blog").all()
        except:
            posts = "Databse is empty"

    return render_template('home/index.html',
                           title='Blog',
                           content=str(posts))


@bundle.route('/screencast', methods=['GET', 'POST'])
@bundle.route('/screencast/', methods=['GET', 'POST'])
@bundle.route('/screencast/<slug>/', methods=['GET', 'POST'])
@bundle.route('/screencast/<slug>', methods=['GET', 'POST'])
def screencast(slug=None):
    if slug is not None:
        try:
            posts = Content.query. \
                filter_by(type_content="screencast").all()
        except:
            posts = "No such content in database."
    else:

        try:
            posts = Content.query. \
                filter_by(type_content="screencast").all()
        except:
            posts = "Databse is empty"

    return render_template('home/index.html',
                           title='screencast',
                           content=str(posts))
