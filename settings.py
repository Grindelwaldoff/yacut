import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('MODIFICATION', default='False')
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        default='qlwrkjsdlfjdlkxmvnawkjrqroisjdfkl23j4lkmsdf2kj'
    )
