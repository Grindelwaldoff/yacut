import re
from random import choices
from urllib.parse import urljoin
from datetime import datetime

from flask import request

from yacut import db
from settings import SHORT_FIELD_LENGTH, SHORT_GENERATE_ALPHABET
from yacut.error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    """Таблица в которой хранятся все ссылки и их вариации."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), nullable=False, default=None)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        if (
            "custom_id" not in data.keys() or
            data["custom_id"] == "" or
            data["custom_id"] is None
        ):
            data.update({"custom_id": self.get_unique_short_id()})
        for field, value in {'url': 'original', 'custom_id': 'short'}.items():
            if field in data:
                if field == 'custom_id':
                    try:
                        if re.search(
                            r'["а-яА-Я!@#$%\s^&*.,:;<>?/\|{}\[\]_+=\-")]',
                            data[field]
                        ):
                            raise InvalidAPIUsage(
                                "Указано недопустимое имя для короткой ссылки",
                                400
                            )
                    except TypeError:
                        pass
                    if len(data[field]) > max(*SHORT_FIELD_LENGTH):
                        raise InvalidAPIUsage(
                            "Указано недопустимое имя для короткой ссылки",
                            400
                        )
                    if self.get(short=data[field]):
                        raise InvalidAPIUsage(
                            f'Имя {data["custom_id"]} уже занято!',
                            400
                        )
            setattr(self, value, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def todict(self):
        return dict(
            short_link=urljoin(request.base_url.replace('api/id/', ''), self.short),
            url=self.original,
        )

    @staticmethod
    def get_unique_short_id():
        return ''.join(choices(SHORT_GENERATE_ALPHABET, k=6))

    @staticmethod
    def get(short):
        # не понял как сдесь можно использовать get()
        return URLMap.query.filter_by(short=short).first()