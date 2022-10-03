import random
import string
from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URL_mapForm
from .models import URL_map


def get_unique_short_id():
    """Генерирование короткого набора символов из букв и цифр."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Страница для создания короткой ссылки."""
    form = URL_mapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if (short_id and
                URL_map.query.filter_by(short=short_id).first() is not None):
            flash(f'Имя {short_id} уже занято!')
            return render_template('index.html', form=form)
        if not short_id:
            short_id = get_unique_short_id()
        url_obj = URL_map(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(url_obj)
        db.session.commit()
        return render_template('index.html', form=form, short_id=short_id)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """Переадресация с короткой на оригинальную ссылку."""
    url_obj = URL_map.query.filter_by(short=short_id).first()
    if url_obj is not None:
        return redirect(url_obj.original)
    abort(HTTPStatus.NOT_FOUND)
