# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from flask.ext.babel import gettext


bundle = Blueprint('api', __name__)

from fedora_college.modules.api.upload import *  # noqa
# Upload media Functions


@bundle.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        json_results = []
        output = {gettext('greetings'):
                  gettext('Welcome to Fedora College api')}
        json_results.append(output)
    return jsonify(items=json_results)
