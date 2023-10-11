import os
from string import ascii_letters, digits


SHORT_GENERATE_ALPHABET = ascii_letters + digits
URL_FIELD_LENGTH = (1, 1000)
SHORT_FIELD_LENGTH = (0, 16)
SHORT_GENERATE_CONST = 6


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('MODIFICATION', default='False')
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        default='qlwrkjsdlfjdlkxmvnawkjrqroisjdfkl23j4lkmsdf2kj'
    )
