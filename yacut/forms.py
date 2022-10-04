from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URL_mapForm(FlaskForm):
    """Форма для создания коротких ссылок."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Regexp('^[A-Za-z0-9]*$',
                   message='Указано недопустимое имя для короткой ссылки'),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
