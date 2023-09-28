from random import choice
from string import ascii_letters


def get_unique_short_id():
    return ''.join(choice(ascii_letters) for i in range(6))
