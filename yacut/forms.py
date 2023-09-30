from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length

from settings import URL_FIELD_LENGTH, SHORT_FIELD_LENGTH


class UrlForm(FlaskForm):
    """Форма для ссылок."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(*URL_FIELD_LENGTH)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(*SHORT_FIELD_LENGTH)]
    )
    submit = SubmitField('Создать')
