# -*- coding: utf-8 -*-
import re
from unicodedata import normalize
from flask import Blueprint, render_template, current_app
from flask import redirect, url_for, g, abort
from sqlalchemy import desc
from fedora_college.core.database import db
from fedora_college.modules.content.forms import *  # noqa
from fedora_college.core.models import *  # noqa
from fedora_college.fedmsgshim import publish
from flask_fas_openid import fas_login_required

bundle = Blueprint('content', __name__, template_folder='templates')

from fedora_college.modules.content.media import *  # noqa


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

# Verify if user is authenticated


def authenticated():
    return hasattr(g, 'fas_user') and g.fas_user

# generate url slug


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

# attach tags to a content entry


def attach_tags(tags, content):
    rem = TagsMap.query.filter_by(content_id=content.content_id).all()
    for r in rem:
        db.session.delete(r)
    db.session.commit()

    for tag in tags:
        tag_db = Tags.query.filter_by(tag_text=tag).first()
        if tag_db is None:
            tag_db = Tags(tag)
            db.session.add(tag_db)
            db.session.commit()
        Map = TagsMap(tag_db.tag_id, content.content_id)
        db.session.add(Map)
    db.session.commit()

# delete content


@bundle.route('/content/delete/<posturl>', methods=['GET', 'POST'])
@bundle.route('/content/delete/<posturl>/', methods=['GET', 'POST'])
@fas_login_required
def delete_content(posturl=None):
    if posturl is not None:
        db.session.rollback()
        content = Content.query.filter_by(slug=posturl).first_or_404()
        rem = TagsMap.query.filter_by(
            content_id=content.content_id).all()
        '''delete mapped tags'''
        for r in rem:
            db.session.delete(r)

        comments = Comments.query.filter_by(
            content_id=content.content_id).all()
        '''delete comments with foriegn keys'''
        for r in comments:
            db.session.delete(r)

        db.session.delete(content)
        db.session.commit()
        return redirect(url_for('profile.user',
                                nickname=g.fas_user['username']))
    abort(404)

# add / edit more content


@bundle.route('/content/add/', methods=['GET', 'POST'])  # noqa
@bundle.route('/content/add', methods=['GET', 'POST'])  # noqa
@bundle.route('/content/edit/<posturl>/', methods=['GET', 'POST'])  # noqa
@bundle.route('/content/edit/<posturl>', methods=['GET', 'POST'])  # noqa
@fas_login_required  # noqa
def addcontent(posturl=None):  # noqa
    if authenticated():
        form = CreateContent()
        form_action = url_for('content.addcontent')
        media = Media.query.order_by(desc(Media.timestamp)).limit(10).all()
        if posturl is not None:
            content = Content.query.filter_by(slug=posturl).first_or_404()
            form = CreateContent(obj=content)
            if form.validate_on_submit():
                form.populate_obj(content)
                tags = str(form.tags.data).split(',')
                attach_tags(tags, content)
                content.rehtml()
                db.session.commit()

                '''Publish the message'''
                msg = content.getdata()
                msg['title'] = content.title
                msg['link'] = current_app.config[
                    'EXTERNAL_URL'] + content.slug
                publish(
                    topic=current_app.config['CONTENT_EDIT_TOPIC'],
                    msg=msg
                )

                if content.type_content == "blog":
                    print url_for('content.blog', slug=posturl)
                    return redirect(url_for('content.blog', slug=posturl))
                return redirect(url_for('home.content', slug=posturl))
        else:
            if form.validate_on_submit():
                url_name = slugify(form.title.data)
                catog = form.category.data.lower()
                content = Content(form.title.data,
                                  url_name,
                                  form.description.data,
                                  form.active.data,
                                  form.tags.data,
                                  g.fas_user['username'],
                                  form.type_content.data,
                                  catog
                                  )
                tags = str(form.tags.data).split(',')
                try:
                    db.session.add(content)
                    db.session.commit()
                    attach_tags(tags, content)

                    '''Publish the message'''
                    msg = content.getdata()
                    msg['title'] = content.title
                    msg['link'] = current_app.config[
                        'EXTERNAL_URL'] + url_name
                    publish(
                        topic=current_app.config['CONTENT_CREATE_TOPIC'],
                        msg=msg
                    )

                    if content.type_content == "blog":
                        return redirect(url_for('content.blog', slug=posturl))
                    return redirect(url_for('home.content', slug=url_name))
                    # Duplicate entry
                except Exception as e:
                    return str(e)
                    db.session.rollback()
                    pass

        tags = Tags.query.all()
        con = Content.query.all()
        lis = []
        for i in con:
            lis.append(i.category)
        lis = set(lis)
        return render_template('content/edit_content.html', form=form,
                               form_action=form_action, title="Create Content",
                               media=media[0:5], tags=tags, cat=lis)
    abort(404)

# View for  Blog post


@bundle.route('/blog', methods=['GET', 'POST'])
@bundle.route('/blog/', methods=['GET', 'POST'])
@bundle.route('/blog/<slug>/', methods=['GET', 'POST'])
@bundle.route('/blog/<slug>', methods=['GET', 'POST'])
@bundle.route('/blog/page/<id>', methods=['GET', 'POST'])
@bundle.route('/blog/page/<id>', methods=['GET', 'POST'])
def blog(slug=None, id=0):
    id = int(id)
    screen = Content.query. \
        filter_by(
            type_content="lecture",
            active=True
        ).limit(10).all()

    if slug is not None:

        try:
            posts = Content.query. \
                filter_by(slug=slug).all()
        except:
            posts = "No such posts in database."
    else:
        try:
            posts = Content.query. \
                filter_by(type_content="blog").all()
            if id > 0:
                posts = posts[id - 1:id + 5]
            else:
                posts = posts[0:5]
        except:
            posts = []
    return render_template('blog/index.html',
                           title='Blog',
                           content=posts,
                           screen=screen,
                           id=id,
                           slug=slug
                           )


@bundle.route('/category', methods=['GET', 'POST'])
@bundle.route('/category/', methods=['GET', 'POST'])
@bundle.route('/categ/<id>', methods=['GET', 'POST'])
@bundle.route('/categ/<id>/', methods=['GET', 'POST'])
@bundle.route('/category/<cat>', methods=['GET', 'POST'])
@bundle.route('/category/<cat>/', methods=['GET', 'POST'])
@bundle.route('/category/<cat>/<id>', methods=['GET', 'POST'])
@bundle.route('/category/<cat>/<id>/', methods=['GET', 'POST'])
def category_view(cat=None, id=0):
    id = int(id)
    lis = []
    screen = Content.query. \
        filter_by(
            active=True
        ).all()
    cats = []
    if cat is None:
        for i in screen:
            cats.append(str(i.category).lower())
        catog = cats[0]
    else:
        for item in screen:
            try:
                if str(item.category).lower() == cat.lower():
                    lis.append(item.getdata())
            except:
                pass
        catog = cat.lower()
        if len(lis) < 1:
            abort(404)
    cats = list(set(cats))
    return render_template('content/cat.html',
                           title='Category View',
                           lis=lis[id:id + 5],
                           len1=len(lis[id:id + 5]),
                           len2=len(cats[id:id + 10]),
                           cat=cats[id:id + 10],
                           id=id,
                           catog= catog
                           )
