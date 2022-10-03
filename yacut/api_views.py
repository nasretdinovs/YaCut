import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Получение оригинальной ссылки из короткой."""
    url_obj = URL_map.query.filter_by(short=short_id).first()
    if url_obj is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_obj.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    """Создание короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_id = data.get('custom_id')
    if (short_id and
            URL_map.query.filter_by(short=short_id).first() is not None):
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    if not short_id:
        short_id = get_unique_short_id()
    if len(short_id) > 16 or not re.match(r'^[A-Za-z0-9]*$', short_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_obj = URL_map(
        original=data['url'],
        short=short_id
    )
    db.session.add(url_obj)
    db.session.commit()
    return jsonify(url_obj.to_dict()), HTTPStatus.CREATED
