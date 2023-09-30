from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.error_handlers import InvalidAPIUsage


@app.route("/api/id/", methods=["POST"])
def create_urlmap():
    data = request.get_json()
    if data is None or {}:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    if (
        "custom_id" not in data.keys() or
        data["custom_id"] == "" or
        data["custom_id"] is None
    ):
        data.update({"custom_id": get_unique_short_id()})
    if URLMap.find_by_short(short=data["custom_id"]):
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.', 400)
    instance = URLMap()
    instance.save(data)
    db.session.add(instance)
    db.session.commit()
    return jsonify(instance.todict()), 201


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_shorted_link(short_id):
    instance = URLMap.query.filter_by(short=short_id).first()
    if instance:
        return jsonify({"url": instance.original}), 200
    raise InvalidAPIUsage("Указанный id не найден", 404)
