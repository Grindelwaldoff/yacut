import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('MODIFICATION')
    SECRET_KEY = os.getenv('SECRET_KEY')
