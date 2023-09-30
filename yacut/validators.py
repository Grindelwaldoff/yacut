import re

from yacut.models import URLMap


def validate_short_id(short_id):
    try:
        if re.search(r'["а-яА-Я!@#$%\s^&*.,:;<>?/\|{}\[\]_+=\-")]', short_id):
            return "Указано недопустимое имя для короткой ссылки", 400
    except TypeError:
        pass
    if URLMap.find_by_short(short=short_id):
        return f'Имя {short_id} уже занято!', 400
    if len(short_id) > 16:
        return "Указано недопустимое имя для короткой ссылки", 400
    return "", 200
