# -*- coding: utf-8 -*-
from sqlalchemy import desc
from flask import Blueprint, render_template
from flask import url_for
from fedora_college.core.models import *  # noqa
from fedora_college.core.database import db
from fedora_college.modules.home.forms import *  # noqa

from urlparse import urljoin
from flask import request
from werkzeug.contrib.atom import AtomFeed


bundle = Blueprint('home', __name__, template_folder='templates')


def make_external(url):
    url = 'blog/' + str(url)
    return urljoin(request.url_root, url)


@bundle.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    articles = Content.query. \
        filter_by(type_content="blog", active=True).limit(30).all()
    for article in articles:
        feed.add(article.title, unicode(article.html),
                 content_type='html',
                 author=article.user_id,
                 url=make_external(article.slug),
                 updated=article.date_added
                 )
    return feed.get_response()


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
        filter_by(type_content="blog", active=True).limit(30).all()

    screen = Content.query. \
        filter_by(type_content="lecture", active=True).limit(30).all()

    return render_template('home/index.html',
                           title='Home',
                           content="Home page",
                           screen=screen,
                           posts=posts)


@bundle.route('/all', methods=['GET', 'POST'])
@bundle.route('/all/', methods=['GET', 'POST'])
@bundle.route('/all/<id>', methods=['GET', 'POST'])
@bundle.route('/all/<id>/', methods=['GET', 'POST'])
def list_all(id=0):
    id = int(id)
    items = []
    result = Content.query. \
        filter_by(type_content="lecture", active=True).all()

    for content in result[id: id + 10]:
        items.append(content)
    return render_template('home/all.html',
                           content=items,
                           title='All ScreenCast',
                           id=id)


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
    star = None
    if authenticated():
        form = AddComment()
        star = None
        form_action = url_for('home.content', slug=slug)
        if form.validate_on_submit():
            query = Comments(form.text.data, form.content_id.data)
            db.session.add(query)
            db.session.commit()
        posts = Content.query.filter_by(
            slug=slug, type_content="lecture").first_or_404()

        if g.fas_user is not None:
            star = Star.query.filter_by(
                username=g.fas_user['username'],
                content_id=posts.content_id
            ).first()
            if star is None:
                star = "UnMarked"
            else:
                star = star.star

        pos.append(posts)
        tree = getcommenttree(posts.content_id)
        return render_template('home/content.html',
                               title='Lecture',
                               content=pos,
                               tree=tree,
                               form=form,
                               form_action=form_action,
                               star=star)
    else:
        posts = Content.query.filter_by(
            slug=slug, type_content="lecture").first_or_404()

        if g.fas_user is not None:
            star = Star.query.filter_by(
                username=g.fas_user['username'],
                content_id=posts.content_id
            ).first()
            if star is None:
                star = "UnMarked"
            else:
                star = star.star

        pos.append(posts)
        tree = getcommenttree(posts.content_id)
        return render_template('home/content.html',
                               title='Lecture',
                               content=pos,
                               tree=tree,
                               star=star
                               )
