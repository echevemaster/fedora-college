# -*- coding: utf-8 -*-
import os
import subprocess
import time
from PIL import Image
import hashlib
from werkzeug import secure_filename
from flask import request, current_app
from fedora_college.core.models import Media
from fedora_college.core.database import db
from fedora_college.fedmsgshim import publish


size = (250, 190)

'''for creating api documentation'''

paths_for_api = {
    "Read": [
        {'parameters': 'None', 'id': '1',
         'name': 'View All Content ',
         'path': '/api/content/', 'methods': 'GET'},
        {'parameters': 'contentid : Number, mostly an integer',
         'id': '2', 'name': 'View Content By ID ',
         'path': '/api/content/<contentid>/', 'methods': 'GET'},
        {'parameters': 'None', 'id': '3',
         'name': 'View All Media',
         'path': '/api/media/', 'methods': 'GET'},
        {'parameters': 'Mediaid : Number, mostly an integer', 'id': '4',
         'name': 'View Media By ID',
         'path': '/api/media/<mediaid>/', 'methods': 'GET'},
        {'parameters': 'None', 'id': '5',
         'name': 'View All User profiles',
         'path': '/api/profile/', 'methods': 'GET'},
        {'parameters': 'Username : Username of any existing user', 'id': '6',
         'name': 'View Profiles By username',
         'path': '/api/profile/<username>/', 'methods': 'GET'},
        {'parameters': 'Keyword: To be searched', 'id': '7',
         'name': 'Perform a Search by keyword',
         'path': '/api/search/<keyword>', 'methods': 'GET'},
        {'parameters': 'None', 'id': '8',
         'name': 'View All Tags',
         'path': '/api/tags/', 'methods': 'GET'},
        {'parameters': 'TagID : Number, mostly an integer', 'id': '9',
         'name': 'View Tags by Tag ID ',
         'path': '/api/tags/<tagid>/', 'methods': 'GET'},
        {'parameters': 'None', 'id': '10',
         'name': 'View Map Tags with Content',
         'path': '/api/tagsmap/', 'methods': 'GET'},
        {'parameters': 'TagID : Number, mostly an integer', 'id': '11',
         'name': 'View MApped Tags with ID',
         'path': '/api/tagsmap/<tagid>/', 'methods': 'GET'},
        {'parameters': 'None', 'id': '12',
         'name': 'API Docs',
         'path': '/api/docs/', 'methods': 'GET'},
        {'parameters': 'None', 'id': '13',
         'name': 'API Home',
         'path': '/api/', 'methods': 'GET'}
    ],
    "Write": [
        {'parameters': 'Access Token : Present in User Profiles  ;  \
         type : Type of file in {video,image,audio,doc}; tags : \
         comma seperated tags  ,featured_name : featured name \
         for file', 'id': '1',
         'name': 'Upload File API',
         'path': '/api/upload/<token>', 'methods': 'POST'},
        {'parameters': 'Access Token : Present in User Profiles  ; \
          Video id : integer', 'id': '3',
         'name': 'Delete file API',
         'path': '/api/upload/delete/<videoid>/<token>', 'methods': 'POST'},
        {'parameters': 'Access Token : Present in User Profiles  ; \
         type = Type of file in {video,image,audio,doc}; tags : \
         comma seperated tags  ,featured_name : featured name\
         for file', 'id': '2',
         'name': 'Upload Revision API',
         'path': '/api/upload/revise/<videoid>/<token>',
         'methods': 'POST, GET'}
    ]
}


''' Function to generate thumbnail '''


def gen_thumbs(data, request, filename, upload_folder, username):
    thumb_path = os.path.join(upload_folder, filename)
    '''
    video
    '''
    if request.form['type'] == 'video':
        name = ('.').join(filename.split('.')[:-1])
        data['thumb'] = "static/uploads/" + \
            str(username) + "/" + str(name) + "_0._thumb.jpg"
        cd = "cd " + upload_folder
        com = cd + " &&  oggThumb -t1 -s240x0 " + \
            filename + "  -o _thumb.jpg"
        print "\n" * 10, com
        subprocess.Popen(com, shell=True)
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

    return data

'''Delete a video '''


def delete(username, videoid):
    obj = Media.query.filter_by(media_id=videoid).first_or_404()
    data = {}
    if obj.user_id == username:
        try:
            db.session.commit()
            db.session.rollback()
            db.session.delete(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'Failed',
                'Reason': 'Please delete associated content',
                'Exception': str(e)
            }

        path = obj.sys_path
        if os.path.isfile(path) and os.access(path, os.R_OK):
            os.remove(path)
        else:
            data['status'] = 'fileNotFound'
            return data['status']
        data['status'] = 'success'
        data['videoid'] = videoid
        data['username'] = username
        return data
    else:
        return {'status': 'Unauthorized'}


'''Generator to buffer file chunks'''


def fbuffer(f, chunk_size=10000):
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        yield chunk


'''write file to disk'''


def write_to_disk(path, filestorage):
    out = open(path, 'wb', 10000)
    for chunk in fbuffer(filestorage.stream):
        out.write(chunk)
    out.close()


''' handling multi part file uploads '''


def upload(username):
    data = {}
    ext = current_app.config['ALLOWED_EXTENSIONS']
    has = hashlib.md5()
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
            last = ""
            for end in ext[str(request.form['type'])]:
                if f.filename.lower().endswith("." + str(end)):
                    proceed = True
                    last = end

            has.update(str(secure_filename(f.filename)))
            filename = str(time.time())
            filename += has.hexdigest() + "." + str(last)
            if proceed is True:
                try:
                    write_to_disk(os.path.join(upload_folder, filename), f)
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
                data['tags'] = request.form['tags']
                data['featured_name'] = request.form['featured_name']

                '''
                    Generate thumbs
                '''
                data = gen_thumbs(
                    data,
                    request,
                    filename,
                    upload_folder,
                    username
                )

            else:
                return {'status': "Error", "Type": "incorrect file type"}
        else:
            return {'status': "Error"}

        data['title'] = filename
        data['link'] = current_app.config['EXTERNAL_URL'] + data['url']
        publish(
            topic=current_app.config['UPLOAD_TOPIC'],
            msg=data)
        return data
    return {'status': "Error"}
