# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template,
                   request, redirect, url_for, g)
from fedora_college.core.database import db
from fedora_college.modules.content.forms import *  # noqa
from fedora_college.core.models import *  # noqa
from flask_fas_openid import fas_login_required

bundle = Blueprint('content', __name__, template_folder='templates')


@bundle.route('/content/add/', methods=['GET', 'POST'])
@bundle.route('/content/add', methods=['GET', 'POST'])
@bundle.route('/content/edit/', methods=['GET', 'POST'])
@bundle.route('/content/edit', methods=['GET', 'POST'])
@bundle.route('/content/edit/<posturl>/', methods=['GET', 'POST'])
@bundle.route('/content/edit/<posturl>', methods=['GET', 'POST'])
@bundle.route('/content/edit/', methods=['GET', 'POST'])
@fas_login_required
def addcontent(posturl=None):
    msg = ""
    form = CreateContent(request.form)
    form_action = url_for('content.addcontent')
    if form.validate():
                msg = "Please validate form"
    if posturl is not None:
        try:
            content = Content.query.filter_by(slug=posturl).first()
            if content is None:
                return str("Not-Found")

            form = CreateContent(obj=content)
            if form.slug.data == content \
                and request.method == 'POST' \
                and form.validate():
                form.populate_obj(content)
                db.session.commit()
                return redirect(url_for('content.addcontent',
                                        posturl=posturl, updated="Content has been updated"))
        except Exception as e:
            # template for not found
            return str("Not-Found : ") + str(e)
    else:
        if request.method == 'POST' \
            and form.validate():
            query = Content(form.title.data,
                            form.slug.data,
                            form.description.data,
                            form.media_added_ids.data,
                            form.active.data,
                            form.tags.data,
                            g.fas_user['username'],
                            form.type_content.data
                            )
            try:
                db.session.add(query)
                db.session.commit()
                # Duplicate entry
            except Exception as e:
                print e
                # template for error
                return (str("Duplicate entry:") + str(e))
            return redirect(url_for('content.addcontent',
                                    posturl=form.slug.data, updated="Content has been Created"))

    return render_template('content/edit_content.html', form=form,
                           form_action=form_action, title="Create Content", updated=msg)


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
