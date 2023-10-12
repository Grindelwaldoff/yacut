import re
from random import choices
from urllib.parse import urljoin
from datetime import datetime

from flask import request

from yacut import db
from settings import (
    SHORT_FIELD_LENGTH, SHORT_GENERATE_ALPHABET,
    URL_FIELD_LENGTH, SHORT_GENERATE_CONST
)


class URLMap(db.Model):
    """Таблица в которой хранятся все ссылки и их вариации."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_FIELD_LENGTH[1]), nullable=False)
    short = db.Column(db.String(SHORT_FIELD_LENGTH[1]), nullable=False, default=None)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def validation(short_id):
        if not re.search(r'^[a-zA-Z0-9]{,16}$', short_id):
            raise ValueError("Указано недопустимое имя для короткой ссылки")
        if URLMap.get(short=short_id):
            raise ValueError('Предложенный вариант короткой ссылки уже существует.')

    @staticmethod
    def from_dict(data):
        url_map = URLMap()
        for field, value in {'url': 'original', 'custom_id': 'short'}.items():
            try:
                setattr(url_map, value, data[field])
            except KeyError:
                pass
        return url_map

    def save(self):
        if self.short in ('', None):
            self.short = URLMap.get_unique_short_id()
        self.validation(self.short)
        db.session.add(self)
        db.session.commit()

    def todict(self):
        return dict(
            short_link=urljoin(request.base_url.replace('api/id/', ''), self.short),
            url=self.original,
        )

    @staticmethod
    def get_unique_short_id():
        return ''.join(choices(SHORT_GENERATE_ALPHABET, k=SHORT_GENERATE_CONST))

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()