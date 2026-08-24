from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .constants import REDIRECT_VIEW
from .error_handlers import InvalidAPIUsage
from .models import URLMap

EMPTY_BODY_MESSAGE = 'Отсутствует тело запроса'
MISSING_FIELD_MESSAGE = '"{}" является обязательным полем!'
NOT_FOUND_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(EMPTY_BODY_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(MISSING_FIELD_MESSAGE.format('url'))
    try:
        url_map = URLMap.create(data['url'], data.get('custom_id'))
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            REDIRECT_VIEW, short=url_map.short, _external=True
        ),
    }), HTTPStatus.CREATED


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    if (url_map := URLMap.get(short)) is None:
        raise InvalidAPIUsage(NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
