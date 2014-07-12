# -*- coding: utf-8 -*-
import re
from unicodedata import normalize
from flask import Blueprint, render_template
from flask import redirect, url_for, g, abort
from sqlalchemy import desc
from fedora_college.core.database import db
from fedora_college.modules.content.forms import *  # noqa
from fedora_college.core.models import *  # noqa
import fedmsg

bundle = Blueprint('content', __name__, template_folder='templates')


from fedora_college.modules.content.media import *  # noqa

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def authenticated():
    return hasattr(g, 'fas_user') and g.fas_user


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


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


@bundle.route('/content/add/', methods=['GET', 'POST'])
@bundle.route('/content/add', methods=['GET', 'POST'])
@bundle.route('/content/edit/<posturl>/', methods=['GET', 'POST'])
@bundle.route('/content/edit/<posturl>', methods=['GET', 'POST'])
def addcontent(posturl=None):
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

                fedmsg.publish(
                    topic='Fedora-college',
                    modname='fedora_college',
                    msg=content
                )
                if content.type_content == "blog":
                    print url_for('content.blog', slug=posturl)
                    return redirect(url_for('content.blog', slug=posturl))
                return redirect(url_for('home.content', slug=posturl))
        else:
            if form.validate_on_submit():
                url_name = slugify(form.title.data)
                query = Content(form.title.data,
                                url_name,
                                form.description.data,
                                form.active.data,
                                form.tags.data,
                                g.fas_user['username'],
                                form.type_content.data
                                )
                tags = str(form.tags.data).split(',')
                try:
                    db.session.add(query)
                    db.session.commit()
                    attach_tags(tags, query)
                    fedmsg.publish(
                        topic='Fedora-college',
                        modname='fedora_college',
                        msg=query
                    )

                    if query.type_content == "blog":
                        return redirect(url_for('content.blog', slug=posturl))
                    return redirect(url_for('home.content', slug=url_name))
                    # Duplicate entry
                except Exception:
                    db.session.rollback()
                    pass

        tags = Tags.query.all()
        return render_template('content/edit_content.html', form=form,
                               form_action=form_action, title="Create Content",
                               media=media, tags=tags)
    abort(404)


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
                           id=id
                           )
