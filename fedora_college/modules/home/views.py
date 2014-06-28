# -*- coding: utf-8 -*-
from sqlalchemy import desc
from flask import Blueprint, render_template
from flask import url_for
from fedora_college.core.models import *  # noqa
from fedora_college.core.database import db
from fedora_college.modules.home.forms import *  # noqa

bundle = Blueprint('home', __name__, template_folder='templates')


def authenticated():
    return hasattr(g, 'fas_user') and g.fas_user


def getcommenttree(content_id):
    tree = []
    query = Comments.query.filter_by(
        content_id=content_id).order_by(desc(Comments.date_added)).all()

    for comment in query:
        tree.append(comment)
    return tree


@bundle.route('/', methods=['GET', 'POST'])
@bundle.route('/index/', methods=['GET', 'POST'])
@bundle.route('/home/', methods=['GET', 'POST'])
def index():
    posts = Content.query. \
        filter_by(type_content="blog").all()

    screen = Content.query. \
        filter_by(type_content="lecture").all()

    return render_template('home/index.html',
                           title='Home',
                           content="Home page",
                           screen=screen,
                           posts=posts)


@bundle.route('/about', methods=['GET', 'POST'])
@bundle.route('/about/', methods=['GET', 'POST'])
def about():
    text = '''
    Acts as a platform for new contributors
    to engage with the community and learn
    how they can contribute best in the community.
    Mostly this service will be used to run online
    courses on contributing at various levels be
    it documentation, bug-fixing or packaging.
    The project would certainly increase the
    activeness in the community and certainly
    make it easy for newer members to craft their
    way around the fedora community. The use of
    virtual classroom environment for training
    new contributors to the community using
    know educational resources by a
    combination of written, images
    and video content.
    '''

    return render_template('home/page.html',
                           text=text,
                           title='About',
                           content='About Us')


@bundle.route('/<slug>/', methods=['GET', 'POST'])
@bundle.route('/<slug>', methods=['GET', 'POST'])
def content(slug=None):
    pos = []
    if authenticated():
        form = AddComment()
        form_action = url_for('home.content', slug=slug)
        if form.validate_on_submit():
            query = Comments(form.text.data, form.content_id.data)
            db.session.add(query)
            db.session.commit()
        posts = Content.query.filter_by(
            slug=slug, type_content="lecture").first_or_404()
        pos.append(posts)
        tree = getcommenttree(posts.content_id)
        return render_template('home/content.html',
                               title='Lecture',
                               content=pos,
                               tree=tree,
                               form=form,
                               form_action=form_action)
    else:
            posts = Content.query.filter_by(
                slug=slug, type_content="lecture").first_or_404()
            pos.append(posts)
            tree = getcommenttree(posts.content_id)
            return render_template('home/content.html',
                                   title='Lecture',
                                   content=pos,
                                   tree=tree)
