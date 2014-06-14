# -*- coding: utf-8 -*-
from flask import (Blueprint,
                   render_template,
                   request)
from fedora_college.core.models import Content

# Upload media Functions
bundle = Blueprint('search', __name__)


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


@bundle.route('/search/', methods=['GET'])
@bundle.route('/search/<keyword>', methods=['GET'])
@bundle.route('/search/<keyword>/', methods=['GET'])
def search(keyword=None):
    if request.args.get('var'):
        keyword = request.args.get('var')
        data = do_search(keyword)
    else:
        data = do_search(keyword)
    return render_template('search/content.html',
                           title='Search',
                           blog=data['blog'],
                           lecture=data['lecture'])
