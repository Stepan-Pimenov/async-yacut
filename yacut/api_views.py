from http import HTTPStatus

from flask import jsonify, request

from . import app
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
        return jsonify({
            'url': data['url'],
            'short_link': URLMap.create(
                data['url'], data.get('custom_id')
            ).get_short_url(),
        }), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    if (url_map := URLMap.get(short)) is None:
        raise InvalidAPIUsage(NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
