# -*- coding: utf-8 -*-
import os
import time
import json
import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug import secure_filename
from fedora_college.core.models import Media, UserProfile
from fedora_college.core.database import db

bundle = Blueprint('api', __name__)


def delete(username, videoid, edit=None):
    media = Media.query.filter_by(media_id=videoid).first_or_404()
    data = {}
    if media.username is username:
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
            filename = str(time.time())
            filename += str(secure_filename(f.filename))
            f.save(os.path.join(upload_folder, filename))
            data['name'] = filename
            data['status'] = 'success'
            data['sys_path'] = os.path.join(upload_folder, filename)
            data['url'] = "static/uploads/" + \
                str(username) + "/" + str(filename)
            data['username'] = username
            data['type'] = request.form['type']
            data['thumb'] = 'static/uploads/' + \
                'thumb' + str(data['name']) + '.jpeg'

            print(data)
        return data
    return {'status': "Error"}


@bundle.route('/api/upload/<token>', methods=['POST'])
def uploadvideo(token):
    data = dict()
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        if user is None:
            return jsonify({'status': 'failed', 'type': 'User Not Found'})

        data = upload(user.username)
        if data['status'] == "success":
            media = Media(data['name'],
                          data['sys_path'],
                          data['url'],
                          user.username,
                          data['type'])
            db.session.add(media)
            db.session.commit()
            return jsonify(data)
        else:
            return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'failed'})


@bundle.route('/api/upload/delete/<videoid>/<token>', methods=['POST'])
def deletevideo(videoid, token):
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        data = delete(user.username, videoid)
        if data['status'] is 'success':
            return jsonify(data)
    else:
        return jsonify({'status': 'failed'})


@bundle.route('/api/upload/revise/<videoid>/<token>', methods=['POST'])
def revisevideo(videoid, token):
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        #data = delete(user.username, videoid, 'yes')
        data = upload(user.username)
        if data['status'] is 'success':
            media = Media.query.filter_by(media_id=videoid).first_or_404()
            old_media = media.getdata()
            media.name = data['name']
            media.content_url = data['url']
            media.sys_path = data['sys_path']
            media.timestamp = datetime.datetime.utcnow()
            old = json.loads(media.revise)
            try:
                old['old'].append(old_media)
            except:
                old = {}
                old['old'] = []
                old['old'].append(old_media)
            media.revise = json.dumps(old)
            db.session.commit()
            return jsonify(data)
    else:
        return jsonify({'status': 'failed'})
