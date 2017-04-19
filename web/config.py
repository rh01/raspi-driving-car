# coding: utf-8

import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "WTForm is What-The-F**k Form"


class DevelopmentConfig(Config):
    BOOTSTRAP_SERVE_LOCAL = True
    DEBUG = True


config = {
    "default": Config, 
    "debug": DevelopmentConfig,
}