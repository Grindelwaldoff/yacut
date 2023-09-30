from random import choices

from settings import SHORT_GENERATE_ALPHABET


def get_unique_short_id():
    return ''.join(choices(SHORT_GENERATE_ALPHABET, k=6))
