from flask import jsonify, request

from yacut import app
from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage


@app.route("/api/id/", methods=["POST"])
def create_urlmap():
    data = request.get_json()
    if data is None or {}:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    answer = URLMap.from_dict(data)
    try:
        answer.save()
    except ValueError as e:
        raise InvalidAPIUsage(str(e), 400)
    return jsonify(answer.todict()), 201


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_shorted_link(short_id):
    instance = URLMap.get(short=short_id)
    if instance:
        return jsonify({"url": instance.original}), 200
    raise InvalidAPIUsage("Указанный id не найден", 404)
