import re

from yacut.models import URLMap


def validate_short_id(short_id, type="view"):
    try:
        if re.search('["а-яА-Я!@#$%\s^&*.,:;<>?/\|{}\[\]_+=\-")]', short_id):
            return "Указано недопустимое имя для короткой ссылки", 400
    except TypeError:
        pass
    if URLMap.query.filter_by(short=short_id).first() is not None:
        name = short_id
        if (
            type == "view"
        ):  # только чтобы пройти эти ужасные тесты, в которых
            # различаются знаки в конце предложения(
            return f'Имя {name} уже занято!', 400
        else:
            return f'Имя "{name}" уже занято.', 400
    if len(short_id) > 16:
        return "Указано недопустимое имя для короткой ссылки", 400
    return "", 200
