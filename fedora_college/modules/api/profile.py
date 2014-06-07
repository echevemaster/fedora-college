# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from fedora_college.core.models import UserProfile

bundle = Blueprint('api', __name__)


@bundle.route('/api/profile', methods=['GET'])
@bundle.route('/api/profile/<username>', methods=['GET'])
@bundle.route('/api/profile/', methods=['GET'])
@bundle.route('/api/profile/<username>/', methods=['GET'])
def profile(username=None):
    if username is not None:
        user = UserProfile.query.filter_by(username=username).first_or_404()
        return jsonify(user.getdata())
    else:
        user = UserProfile.query.all()
        data = {}
        for i in user:
            data[i.user_id] = i.getdata()
        return jsonify(data)


@bundle.route('/api/profile/edit/<token>', methods=['GET'])
@bundle.route('/api/profile/edit/<token>/', methods=['GET'])
def editprofile(token=None):
    if (token is not None):
        user = UserProfile.query.filter_by(token=token).first_or_404()
        return jsonify(user.getdata())
    return "None"
