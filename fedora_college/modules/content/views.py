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
@bundle.route('/content/edit/<posturl>/', methods=['GET', 'POST'])
@bundle.route('/content/edit/<posturl>', methods=['GET', 'POST'])
@fas_login_required
def addcontent(posturl=None):
    form = CreateContent()
    form_action = url_for('content.addcontent')
    if posturl is not None:
        content = Content.query.filter_by(slug=posturl).first_or_404()
        form = CreateContent(obj=content)

        if form.slug.data == posturl and request.method == 'POST' and form.validate():
            form.populate_obj(content)
            db.session.commit()
            return redirect(url_for('content.addcontent',
                                    posturl=posturl, updated="True"))
    else:
        if request.method == 'POST' and form.validate():
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
            except Exception as e:                
                # Duplicate entry
                return str(e)
            return redirect(url_for('content.addcontent',
                                    posturl=form.slug.data, updated="True"))
        else:
            print "Please validate form"
    return render_template('content/edit_content.html', form=form,
                           form_action=form_action, title="Create Content")


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

    return render_template('blog/index.html',
                           title='Blog',
                           content=posts)
