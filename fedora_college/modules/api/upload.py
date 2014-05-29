# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug import secure_filename
from fedora_college.core.models import Media, UserProfile
from fedora_college.core.database import db

bundle = Blueprint('api', __name__)


def delete(username, videoid, edit=None):
    media = Media.query.filter_by(media_id=videoid).first_or_404()
    data = {}
    if media.username == username:
        path = media.sys_path
        if os.path.isfile(path) and os.access(path, os.R_OK):
            os.remove(path)
        else:
            data['status'] = 'fileNotFound'
            return data['status']
        if edit is not None:
            db.session.commit()
        else:
            db.session.delete(media)
        data['status'] = 'success'
        data['videoid'] = videoid
        data['username'] = username
        return data
    else:
        return {'status': 'Unauthorized'}


def upload(username):
    data = {}
    if request.method == 'POST':
        path = current_app.config['UPLOADS_FOLDER'] + str(username) + "/"
        upload_folder = os.path.join(path)
        if not os.path.exists(upload_folder):
            os.mkdir(upload_folder)

        f = request.files['file']
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(upload_folder, filename))
            data['name'] = filename
            data['status'] = 'success'
            data['sys_path'] = os.path.join(upload_folder, filename)
            data['username'] = username
        return data
    return {'status': "Error"}


@bundle.route('/api/upload/<token>', methods=['POST'])
def uploadVideo(token):
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        data = upload(user.username)
        if data['status'] == 'success':
            media = Media(data['filename'], data[
                          'sys_path'], data['sys_path'], user.username)
            db.session.add(media)
            db.session.commit()
            return jsonify(data)
    else:
        return jsonify({'status': 'failed'})


@bundle.route('/api/upload/delete/<videoid>/<token>', methods=['POST'])
def deletevideo(videoid, token):
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        data = delete(user.username, videoid)
        if data['status'] == 'success':
            return jsonify(data)
    else:
        return jsonify({'status': 'failed'})


@bundle.route('/api/upload/revise/<videoid>/<token>', methods=['POST'])
def revisevideo(videoid, token):
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        data = delete(user.username, videoid, 'yes')
        if data['status'] == 'success':
            data = upload(user.username)
            if data['status'] == 'success':
                media = Media.query.filter_by(media_id=videoid).first_or_404()
                media.name = data['filename']
                media.content_url = data['sys_path']
                media.sys_path = data['sys_path']
                media.timestamp = db.Column(db.DateTime())
                db.session.commit()
                return jsonify(data)
    else:
        return jsonify({'status': 'failed'})
