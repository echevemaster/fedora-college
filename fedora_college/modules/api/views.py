# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug import secure_filename
from flask.ext.babel import gettext


bundle = Blueprint('api', __name__)

from fedora_college.modules.api.upload import *  # noqa # Upload media Functions 

@bundle.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        json_results = []
        output = {gettext('greetings'):
                  gettext('Welcome to Fedora College api')}
        json_results.append(output)
    return jsonify(items=json_results)

