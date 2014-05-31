from flask import Blueprint, render_template
from flask import url_for, g
from fedora_college.modules.content.forms import *  # noqa
from fedora_college.core.models import *  # noqa

bundle = Blueprint('content', __name__, template_folder='templates')


@bundle.route('/media/add/', methods=['GET', 'POST'])
@bundle.route('/media/add', methods=['GET', 'POST'])
def uploadmedia():
    user = UserProfile.query. \
        filter_by(username=g.fas_user['username']).first_or_404()
    token = user.token
    form_action = url_for('api.uploadvideo', token=token)
    return render_template('media/uploadmedia.html', /
           form_action=form_action, title="add media")


@bundle.route('/media/view')
@bundle.route('/media/view/')
@bundle.route('/media/view/<mediaid>')
@bundle.route('/media/view/<mediaid>/')
def displaymedia(mediaid=None):
    url = url_for('content.displaymedia')
    if mediaid is not None:
        media = Media.query.filter_by(media_id=mediaid).all()
        return render_template('media/index.html', data=media, url=url)
    else:
        media = Media.query.all()
        return render_template('media/index.html', data=media, url=url)


@bundle.route('/media/view/<mediaid>/revise')
@bundle.route('/media/view/<mediaid>/revise/')
def revisemedia():
    media = Media.query.filter_by(media_id=mediaid).all()
    return render_template('media/revise.html', id=mediaid, media=media)
