from datetime import datetime
from urllib.parse import urljoin

from flask import request

from yacut import db


class URLMap(db.Model):
    """Таблица в которой хранятся все ссылки и их вариации."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), nullable=False, default=None)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def _fromdict(self, data):
        for field, value in {'url': 'original', 'custom_id': 'short'}.items():
            if field in data:
                setattr(self, value, data[field])

    def _todict(self):
        return dict(
            short_link=urljoin(request.base_url.replace('api/id/', ''), self.short),
            url=self.original,
        )
