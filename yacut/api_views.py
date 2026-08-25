from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

URL_KEY = 'url'
EMPTY_BODY_MESSAGE = 'Отсутствует тело запроса'
MISSING_FIELD_MESSAGE = f'"{URL_KEY}" является обязательным полем!'
NOT_FOUND_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(EMPTY_BODY_MESSAGE)
    if URL_KEY not in data:
        raise InvalidAPIUsage(MISSING_FIELD_MESSAGE)
    try:
        return jsonify({
            URL_KEY: data[URL_KEY],
            'short_link': URLMap.create(
                data[URL_KEY], data.get('custom_id')
            ).get_short_url(),
        }), HTTPStatus.CREATED
    except (ValueError, RuntimeError) as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    if (url_map := URLMap.get(short)) is None:
        raise InvalidAPIUsage(NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({URL_KEY: url_map.original}), HTTPStatus.OK
