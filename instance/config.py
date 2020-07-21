import os

class Config(object):
    SECRET_KEY = 'Ar2098urd'
    POSTS_PER_PAGE = 10

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Ar2098urd@localhost/forum?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False