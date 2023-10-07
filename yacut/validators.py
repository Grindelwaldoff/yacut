import re

from yacut.models import URLMap
from settings import SHORT_FIELD_LENGTH


def validate_short_id(short_id):
    try:
        if re.search(r'["а-яА-Я!@#$%\s^&*.,:;<>?/\|{}\[\]_+=\-")]', short_id):
            return "Указано недопустимое имя для короткой ссылки"
    except TypeError:
        pass
    if URLMap.get(short=short_id):
        return 'Предложенный вариант короткой ссылки уже существует.'
    if len(short_id) > max(*SHORT_FIELD_LENGTH):
        return "Указано недопустимое имя для короткой ссылки"
