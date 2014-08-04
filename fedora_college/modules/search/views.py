# -*- coding: utf-8 -*-
from flask import (Blueprint,
                   render_template,
                   request)
from fedora_college.core.models import Content, Media

# Upload media Functions
bundle = Blueprint('search', __name__, url_prefix='/search')


def do_search(keyword):
    data = {}
    data['blog'] = []
    data['lecture'] = []
    if keyword is not None:
        result = Content.query.whoosh_search(keyword).all()
        for obj in result:
            if obj.type_content == "blog":
                data['blog'].append(obj.getdata())
            else:
                data['lecture'].append(obj.getdata())
    return data


def do_media_search(keyword):
    data = {}
    data['media'] = []
    if keyword is not None:
        result = Media.query.whoosh_search(keyword).all()
        if result is None:
            data['media'] = ['Nothing']
            return data
        for obj in result:
            data['media'].append(obj.getdata())
    return data


@bundle.route('/media/', methods=['GET'])
@bundle.route('/media/<keyword>', methods=['GET'])
@bundle.route('/media/<keyword>/', methods=['GET'])
def media_search(keyword=None):
    data = {}
    if request.args.get('var'):
        keyword = request.args.get('var')
        data = do_media_search(keyword)
    elif keyword is not None:
        data = do_media_search(keyword)
    else:
        data['media'] = None

    if len(data['media']) < 1:
        data['media'] = None
    return render_template('search/media.html',
                           title='Search',
                           media=data['media']
                           )


@bundle.route('/', methods=['GET'])
@bundle.route('/<keyword>', methods=['GET'])
@bundle.route('/<keyword>/', methods=['GET'])
@bundle.route('/<keyword>/<id>', methods=['GET'])
@bundle.route('/<keyword>/<id>/', methods=['GET'])
def search(keyword=None, id=0):
    id = int(id)
    if request.args.get('var'):
        keyword = request.args.get('var')
        data = do_search(keyword)
    else:
        data = do_search(keyword)
        if id > 0:
            data['blog'] = data['blog'][id:id + 10]
            data['lecture'] = data['lecture'][id:id + 10]
    return render_template('search/content.html',
                           title='Search',
                           blog=data['blog'],
                           lecture=data['lecture'],
                           keyword=keyword,
                           id=id)
