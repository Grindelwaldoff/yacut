import re
from random import choices
from datetime import datetime
from urllib.parse import urljoin

from flask import request

from yacut import db
from settings import SHORT_GENERATE_ALPHABET
from yacut.error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    """Таблица в которой хранятся все ссылки и их вариации."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), nullable=False, default=None)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
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
                    if len(data[field]) > 16:
                        raise InvalidAPIUsage(
                            "Указано недопустимое имя для короткой ссылки",
                            400
                        )
                    # if URLMap.find_by_short(data[field]):
                    #     raise InvalidAPIUsage(
                    #         f'Имя "{data[field]}" уже занято.', 400
                    #     )
            setattr(self, value, data[field])

    @staticmethod
    def get_unique_short_id():
        return ''.join(choices(SHORT_GENERATE_ALPHABET, k=6))

    def save(self, db):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return dict(
            short_link=urljoin(request.base_url.replace('api/id/', ''), self.short),
            url=self.original,
        )

    @staticmethod
    def find_by_short(short):
        # не понял как сдесь можно использовать get()
        return URLMap.query.filter_by(short=short).first()