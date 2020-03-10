from os import environ

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = True