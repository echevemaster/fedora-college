# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug import secure_filename
from flask.ext.babel import gettext

bundle = Blueprint('api', __name__)

@bundle.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        json_results = []
        output = {gettext('greetings'): gettext('Welcome to Fedora College api')}
        json_results.append(output)
    return jsonify(items=json_results)

@bundle.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        upload_folder = os.path.join(current_app.config['UPLOADS_FOLDER'])
        if not os.path.exists(upload_folder):
            os.mkdir(upload_folder)
            print upload_folder
        files = []
        f = request.files['file']
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(upload_folder, filename))
        output = {
            'name': filename,
            'status': 'success'
        }
        files.append(output)
    return jsonify(files=files)
