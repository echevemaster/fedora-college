# -*- coding: utf-8 -*-
import json
import datetime
from flask.ext.babel import gettext
from flask import Blueprint, request, jsonify
from fedora_college.core.models import Media, UserProfile
from fedora_college.core.models import Tags, TagsMap
from fedora_college.core.models import Content
from fedora_college.core.database import db
from fedora_college.modules.api.helper import paths_for_api, delete, upload

# Upload media Functions
bundle = Blueprint('api', __name__)


@bundle.route('/api/', methods=['GET'])
@bundle.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        json_results = []
        output = {gettext('greetings'):
                  gettext('Welcome to Fedora College api'),
                  'documentation': '/api/docs/'}
        json_results.append(output)
    return jsonify(items=json_results)


@bundle.route('/api/docs', methods=['GET'])
@bundle.route('/api/docs/', methods=['GET'])
def docs():
    if request.method == 'GET':
        json_results = []
        json_results.append(paths_for_api)
    return jsonify(paths=json_results)


@bundle.route('/api/tags', methods=['GET'])
@bundle.route('/api/tags/', methods=['GET'])
@bundle.route('/api/tags/<tagid>', methods=['GET'])
@bundle.route('/api/tags/<tagid>/', methods=['GET'])
def tagsview(tagid=None):
    json_results = {}
    if request.method == 'GET':
        if tagid is not None:
            tag = Tags.query.filter_by(tag_id=tagid).first()
            if tag is None:
                json_results = {tagid: "None"}
            else:
                json_results = tag.getdata()
        else:
            tags = Tags.query.all()
            for tag in tags:
                json_results[tag.tag_id] = tag.getdata()
    return jsonify(json_results)


@bundle.route('/api/tags/map', methods=['GET'])
@bundle.route('/api/tags/map/', methods=['GET'])
@bundle.route('/api/tags/map/<tagid>', methods=['GET'])
@bundle.route('/api/tags/map/<tagid>/', methods=['GET'])
def tagsmapview(tagid=None):
    json_results = {}
    json_results['tags'] = []
    if request.method == 'GET':
        if tagid is not None:
            tags = TagsMap.query.filter_by(tag_id=tagid).all()
            for tag in tags:
                json_results['tags'].append(tag.getdata())
        else:
            tags = TagsMap.query.all()
            for tag in tags:
                json_results['tags'].append(tag.getdata())
    json_results['count'] = len(json_results['tags'])
    return jsonify(json_results)


@bundle.route('/api/profile', methods=['GET'])
@bundle.route('/api/profile/', methods=['GET'])
@bundle.route('/api/profile/<username>', methods=['GET'])
@bundle.route('/api/profile/<username>/', methods=['GET'])
def profileview(username=None):

    if request.method == 'GET':
        if username is not None:
            user = UserProfile.query.filter_by(username=username).first()
            return jsonify(user.getdata())
        else:
            users = UserProfile.query.all()
            data = {}
            data['users'] = []
            for user in users:
                data['users'].append(user.getdata())
            data['count'] = len(data['users'])
            return jsonify(data)
    else:
        return jsonify({})


@bundle.route('/api/content', methods=['GET'])
@bundle.route('/api/content/', methods=['GET'])
@bundle.route('/api/content/<contentid>', methods=['GET'])
@bundle.route('/api/content/<contentid>/', methods=['GET'])
def contentview(contentid=None):
    json_results = {}
    json_results['content'] = []
    if request.method == 'GET':
        if contentid is not None:
            content = Content.query.filter_by(content_id=contentid).first()
            if content is None:
                json_results['content'].append({contentid: "None"})
            else:
                json_results['content'].append(content.getdata())
        else:
            content = Content.query.all()
            for content in content:
                json_results['content'].append(content.getdata())
    json_results['count'] = len(json_results['content'])
    return jsonify(json_results)


@bundle.route('/api/media', methods=['GET'])
@bundle.route('/api/media/', methods=['GET'])
@bundle.route('/api/media/<mediaid>', methods=['GET'])
@bundle.route('/api/media/<mediaid>/', methods=['GET'])
def mediaview(mediaid=None):
    json_results = {}
    json_results['media'] = []
    if request.method == 'GET':
        if mediaid is not None:
            media = Media.query.filter_by(media_id=mediaid).first_or_404()
            if media is None:
                json_results['media'].append({mediaid: "None"})
            else:
                json_results['media'].append(media.getdata())
        else:
            media = Media.query.all()
            for media in media:
                json_results['media'].append(media.getdata())
    json_results['count'] = len(json_results['media'])
    return jsonify(json_results)


@bundle.route('/api/search/<keyword>', methods=['GET'])
@bundle.route('/api/search/<keyword>', methods=['GET'])
def search(keyword=None):
    data = {}
    data['blog'] = []
    data['lecture'] = []
    if data is not None:
        result = Content.query.whoosh_search(keyword).all()
        for obj in result:
            if obj.type_content == "blog":
                data['blog'].append(obj.getdata())
            else:
                data['lecture'].append(obj.getdata())
    return jsonify(data)


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
                          data['type'],
                          data['thumb'])
            db.session.add(media)
            db.session.commit()
            return jsonify(data)
        else:
            return jsonify(data)
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
            media.thumb_url = data['thumb']
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
