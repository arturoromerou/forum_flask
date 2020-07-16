import os

class Config(object):
    SECRET_KEY = 'Ar2098urd'

class DevelopmentConfig(Config):
    DEBUG = True