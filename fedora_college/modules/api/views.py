# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify

bundle = Blueprint('api', __name__)


@bundle.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        json_results = []
        output = {'greetings': 'Welcome to Fedora College api'}
        json_results.append(output)
    return jsonify(items=json_results)
