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
from yacut.error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    """Таблица в которой хранятся все ссылки и их вариации."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_FIELD_LENGTH[1]), nullable=False)
    short = db.Column(db.String(SHORT_FIELD_LENGTH[1]), nullable=False, default=None)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def validation(short_id):
        try:
            if not re.search(r'^[a-zA-Z0-9]+$', short_id):
                return "Указано недопустимое имя для короткой ссылки"
        except TypeError:
            pass
        if URLMap.get(short=short_id):
            return 'Предложенный вариант короткой ссылки уже существует.'
        if len(short_id) > max(*SHORT_FIELD_LENGTH):
            return "Указано недопустимое имя для короткой ссылки"

    @staticmethod
    def from_dict(data):
        url_map = URLMap()
        for field, value in {'url': 'original', 'custom_id': 'short'}.items():
            try:
                if field == 'custom_id' and data[field] not in ('', None):
                    error_msg = URLMap.validation(data[field])
                    if error_msg:
                        return error_msg
                setattr(url_map, value, data[field])
            except KeyError:
                pass
        return url_map

    def save(self):
        if self.short in ('', None):
            setattr(self, 'short', URLMap.get_unique_short_id())
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
        # не понял как сдесь можно использовать get()
        return URLMap.query.filter_by(short=short).first()