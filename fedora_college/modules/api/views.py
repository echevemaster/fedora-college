# -*- coding: utf-8 -*-
import json
import datetime
from flask.ext.babel import gettext
from flask import Blueprint, request, jsonify, redirect
from flask import url_for, g, abort, render_template
from fedora_college.core.models import Media, UserProfile
from fedora_college.core.models import Tags, TagsMap
from fedora_college.core.models import Content, Vote, Star
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
        data = paths_for_api
        return render_template('api/api.html',
                               read=data['Read'],
                               write=data['Write'])
    abort(404)


@bundle.route('/api/tags', methods=['GET'])
@bundle.route('/api/tags/', methods=['GET'])
@bundle.route('/api/tags/<id>', methods=['GET'])
@bundle.route('/api/tags/<id>/', methods=['GET'])
@bundle.route('/api/tags/<tagid>/<id>', methods=['GET'])
@bundle.route('/api/tags/<tagid>/<id>/', methods=['GET'])
def tagsview(tagid=None, id=0):
    id = int(id)
    json_results = {}
    if request.method == 'GET':
        if tagid is not None:
            tag = Tags.query.filter_by(tag_id=tagid).first_or_404()
            if tag is None:
                json_results = {tagid: "None"}
            else:
                json_results = tag.getdata()
        else:
            tags = Tags.query.all()
            for tag in tags[id:id + 10]:
                json_results[tag.tag_id] = tag.getdata()
    return jsonify(
        items=json_results,
        next=url_for('api.tagsview', id=id + 10)
    )


@bundle.route('/api/tagsmap', methods=['GET'])
@bundle.route('/api/tagsmap/', methods=['GET'])
@bundle.route('/api/tagsmap/<id>', methods=['GET'])
@bundle.route('/api/tagsmap/<id>/', methods=['GET'])
@bundle.route('/api/tagsmap/<tagid>', methods=['GET'])
@bundle.route('/api/tagsmap/<tagid>/', methods=['GET'])
def tagsmapview(tagid=None, id=0):
    id = int(id)
    json_results = {}
    json_results['tags'] = []
    if request.method == 'GET':
        if tagid is not None:
            tags = TagsMap.query.filter_by(tag_id=tagid).all()
            for tag in tags:
                json_results['tags'].append(tag.getdata())
        else:
            tags = TagsMap.query.all()
            for tag in tags[id:id + 10]:
                json_results['tags'].append(tag.getdata())
    json_results['count'] = len(json_results['tags'])
    return jsonify(
        items=json_results,
        next=url_for('api.tagsmapview', id=id + 10)
    )


@bundle.route('/api/profile', methods=['GET'])
@bundle.route('/api/profile/', methods=['GET'])
@bundle.route('/api/profile/<id>', methods=['GET'])
@bundle.route('/api/profile/<id>/', methods=['GET'])
@bundle.route('/api/profile/<username>', methods=['GET'])
@bundle.route('/api/profile/<username>/', methods=['GET'])
def profileview(username=None, id=0):
    id = int(id)
    if request.method == 'GET':
        if username is not None:
            user = UserProfile.query.filter_by(
                username=username).first_or_404()
            return jsonify(user.getdata())
        else:
            users = UserProfile.query.all()
            data = {}
            data['users'] = []
            for user in users[id:id + 10]:
                data['users'].append(user.getdata())
            data['count'] = len(data['users'])
            return jsonify(
                items=data,
                next=url_for('api.tagsmapview', id=id + 10)
            )
    else:
        return jsonify({})


@bundle.route('/api/content', methods=['GET'])
@bundle.route('/api/content/', methods=['GET'])
@bundle.route('/api/content/<id>', methods=['GET'])
@bundle.route('/api/content/<id>/', methods=['GET'])
@bundle.route('/api/content/<contentid>', methods=['GET'])
@bundle.route('/api/content/<contentid>/', methods=['GET'])
def contentview(contentid=None, id=0):
    id = int(id)
    json_results = {}
    json_results['content'] = []
    if request.method == 'GET':
        if contentid is not None:
            content = Content.query.filter_by(
                content_id=contentid).first_or_404()
            if content is None:
                json_results['content'].append({contentid: "None"})
            else:
                json_results['content'].append(content.getdata())
        else:
            content = Content.query.all()
            for content in content[id:id + 10]:
                json_results['content'].append(content.getdata())
            json_results['next'] = url_for('api.contentview', id=id + 10)
    json_results['count'] = len(json_results['content'])

    return jsonify(json_results)


@bundle.route('/api/media', methods=['GET'])
@bundle.route('/api/media/', methods=['GET'])
@bundle.route('/api/media/<id>', methods=['GET'])
@bundle.route('/api/media/<id>/', methods=['GET'])
@bundle.route('/api/media/<mediaid>', methods=['GET'])
@bundle.route('/api/media/<mediaid>/', methods=['GET'])
def mediaview(mediaid=None, id=0):
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
            for media in media[id:id + 10]:
                json_results['media'].append(media.getdata())
            json_results['next'] = url_for('api.mediaview', id=id + 10)
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
@bundle.route('/api/upload/<token>/', methods=['POST'])
@bundle.route('/api/upload/<token>/<url>/', methods=['POST'])
@bundle.route('/api/upload/<token>/<url>/', methods=['POST'])
def uploadvideo(token, url=None):
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
                          data['thumb'],
                          data['tags'],
                          data['featured_name'])
            db.session.add(media)
            db.session.commit()
            if url is not None:
                url = url_for('content.displaymedia')
                return redirect(url)
            return jsonify(data)
        else:
            return jsonify(data)
    else:
        return jsonify({'status': 'failed'})


@bundle.route('/api/upload/delete/<videoid>/<token>', methods=['GET', 'POST'])
def deletevideo(videoid, token):
    db.session.rollback()
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        data = delete(user.username, videoid)
        return jsonify(data)
    else:
        return jsonify(
            {'status': 'failed',
             'Reason': 'Please give a valid user acess Token'
             })


@bundle.route('/api/upload/revise/<videoid>/<token>', methods=['POST'])
def revisevideo(videoid, token):
    if token is not None:
        user = UserProfile.query. \
            filter_by(token=token).first_or_404()
        # data = delete(user.username, videoid, 'yes')
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


''' Private API funtion
    These will only work with session
'''


@bundle.route('/api/echorequest', methods=['GET', 'POST'])
@bundle.route('/api/echorequest/', methods=['GET', 'POST'])
def echo():
    if request.method == 'POST' and g.fas_user['username'] is not None:

        rating = int(request.values['rate'])
        content_id = int(request.values['idBox'])

        username = g.fas_user['username']

        data = dict()
        data['message'] = 'hello, ' + str(username)
        data['server'] = "You have already Voted"

        query = Vote.query.filter_by(
            username=username,
            content_id=content_id
        ).first()

        if query is None:
            vote = Vote(rating, content_id, username)
            db.session.add(vote)
            db.session.commit()
            data['server'] = "Thanks for your vote"

        return jsonify(data)
    abort(404)


@bundle.route('/api/addstar/<content>/<slug>/', methods=['GET', 'POST'])
@bundle.route('/api/addstar/<content>/<slug>', methods=['GET', 'POST'])
def mark_star(content=None, slug=None):

    if content is not None and g.fas_user['username'] is not None:
        username = g.fas_user['username']
        query = Star.query.filter_by(
            username=username,
            content_id=content
        ).first()

        if query is None:
            query = Star("Marked", content, username)
            db.session.add(query)
        else:
            if query.star == "Marked":
                query.star = "UnMarked"
            else:
                query.star = "Marked"
        db.session.commit()
        return redirect(url_for('home.content', slug=slug))
    abort(404)
