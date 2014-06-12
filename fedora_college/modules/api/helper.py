# -*- coding: utf-8 -*-
import os
import time
from PIL import Image
from werkzeug import secure_filename
from flask import request, current_app
from fedora_college.core.models import Media
from fedora_college.core.database import db

size = (120, 120)
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
    "Write": [
        {'path': '/api/upload/<token>', 'methods': 'POST'},
        {'path': '/api/upload/delete/<videoid>/<token>', 'methods': 'POST'},
        {'path': '/api/upload/revise/<videoid>/<token>', 'methods': 'POST'}
    ]
}


def gen_thumbs(data, request, filename):
    if request.form['type'] == 'video':
        name = ('.').join(filename.split('.')[:-1])
        data['thumb'] = "static/uploads/" + \
            str(username) + "/" + str(name) + "_0._thumb.jpg"
        cd = "cd " + upload_folder
        com = cd + " &&  oggThumb -t1 -s240x0 " + \
            filename + " -o _thumb.jpg"
        os.system(com)
    '''
    Image
    '''
    if request.form['type'] == 'image':
        name = ('.').join(filename.split('.')[:-1])
        data['thumb'] = "static/uploads/" + \
            str(username) + "/" + str(filename) + "_thumb.jpg"
        im = Image.open(data['sys_path'])
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(thumb_path + "_thumb.jpg", "JPEG")

    if request.form['type'] == 'audio':
        data['thumb'] = "static/images/audio_thumb.gif"

    if request.form['type'] == 'doc':
        data['thumb'] = "static/images/doc_thumb.gif"


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
    ext = current_app.config['ALLOWED_EXTENSIONS']
    if request.method == 'POST':
        path = current_app.config['UPLOADS_FOLDER'] + str(username) + "/"
        upload_folder = os.path.join(path)
        if not os.path.exists(upload_folder):
            os.mkdir(upload_folder)

        f = request.files['file']
        if f:
            filename = str(time.time())
            filename += str(secure_filename(f.filename))
            proceed = False
            for end in ext[str(request.form['type'])]:
                if f.filename.lower().endswith("." + str(end)):
                    proceed = True
            if proceed is True:
                try:
                    f.save(os.path.join(upload_folder, filename))
                except Exception as e:
                    return {'status': "Error", 'error': str(e)}

                data['name'] = filename
                data['status'] = 'success'
                data['sys_path'] = os.path.join(upload_folder, filename)
                data['url'] = "static/uploads/" + \
                    str(username) + "/" + str(filename)
                data['username'] = username
                data['type'] = request.form['type']
                data['thumb'] = ""
                thumb_path = os.path.join(upload_folder, filename)

                '''
                    Generate thumbs
                '''
                data = gen_thumbs(
                    data,
                    request,
                    filename,
                    upload_folder
                )
            else:
                return {'status': "Error", "Type": "incorrect file type"}
        else:
            return {'status': "Error"}
        return data
    return {'status': "Error"}
