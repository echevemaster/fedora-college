# -*- coding: utf-8 -*-
import os
import time
import json
from werkzeug import secure_filename
from flask import request, current_app

paths_for_api = {
    "Read": [
    {'path': '/api/content/', 'methods': 'GET'},
    {'path': '/api/content/<contentid>/', 'methods': 'GET'},

    {'path': '/api/media/', 'methods': 'GET'},
    {'path': '/api/media/<mediaid>/', 'methods': 'GET'},

    {'path': '/api/profile/', 'methods': 'GET'},
    {'path': '/api/profile/<username>/', 'methods': 'GET'},

    {'path': '/api/tags/', 'methods': 'GET'},
    {'path': '/api/tags/<tagid>/', 'methods': 'GET'},

    {'path': '/api/tags/map/', 'methods': 'GET'},
    {'path': '/api/tags/map/<tagid>/', 'methods': 'GET'},

    {'path': '/api/docs/', 'methods': 'GET'},
    {'path': '/api/', 'methods': 'GET'}
    ],
    "Write":
    [
    {'path': '/api/upload/<token>', 'methods': 'POST'},
    {'path': '/api/upload/delete/<videoid>/<token>', 'methods': 'POST'},
    {'path': '/api/upload/revise/<videoid>/<token>', 'methods': 'POST'}
    ]
}


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
