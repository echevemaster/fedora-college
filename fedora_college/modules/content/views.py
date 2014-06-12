# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask import redirect, url_for, g
from fedora_college.core.database import db
from fedora_college.modules.content.forms import *  # noqa
from fedora_college.core.models import *  # noqa
from flask_fas_openid import fas_login_required

bundle = Blueprint('content', __name__, template_folder='templates')


from fedora_college.modules.content.media import *  # noqa


def attach_tags(tags, content):
    for tag in tags:
        tag_db = Tags.query.filter_by(tag_text=tag).first()
        if tag_db is None:
            tag_db = Tags(tag)
        db.session.add(tag_db)
        Map = TagsMap(tag_db.tag_id, content.content_id)
        db.session.add(Map)
    db.session.commit()


@bundle.route('/content/add/', methods=['GET', 'POST'])
@bundle.route('/content/add', methods=['GET', 'POST'])
@bundle.route('/content/edit/<posturl>/', methods=['GET', 'POST'])
@bundle.route('/content/edit/<posturl>', methods=['GET', 'POST'])
@fas_login_required
def addcontent(posturl=None):
    media = Media.query.filter_by(user_id=g.fas_user['username']).all()
    form = CreateContent()
    form_action = url_for('content.addcontent')
    if posturl is not None:
        content = Content.query.filter_by(slug=posturl).first_or_404()
        form = CreateContent(obj=content)
        if form.slug.data == posturl and form.validate_on_submit():
            form.populate_obj(content)
            tags = str(form.tags.data).split(',')

            attach_tags(tags, content)
            db.session.commit()
            return redirect(url_for('content.addcontent',
                                    posturl=posturl,
                                    updated="Successfully updated")
                            )

    else:
        if form.validate_on_submit():
            query = Content(form.title.data,
                            form.slug.data,
                            form.description.data,
                            form.media_added_ids.data,
                            form.active.data,
                            form.tags.data,
                            g.fas_user['username'],
                            form.type_content.data
                            )
            tags = str(form.tags.data).split(',')
            attach_tags(tags, query)
            try:
                db.session.add(query)
                db.session.commit()

                # Duplicate entry
            except Exception as e:
                print e

            return redirect(url_for('content.addcontent',
                                    posturl=form.slug.data,
                                    media =media,
                                    updated="Successfully updated")
                            )
        else:
            print "Please validate form"
    return render_template('content/edit_content.html',
                           form=form,
                           form_action=form_action,
                           media = media,
                           title="Create Content")


@bundle.route('/blog', methods=['GET', 'POST'])
@bundle.route('/blog/', methods=['GET', 'POST'])
@bundle.route('/blog/<slug>/', methods=['GET', 'POST'])
@bundle.route('/blog/<slug>', methods=['GET', 'POST'])
def blog(slug=None):
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
        except:
            posts = "Databse is empty"

    return render_template('blog/index.html',
                           title='Blog',
                           content=posts)
