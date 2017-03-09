# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('NORMAN_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGOALCHEMY_DATABASE = "norman"
    APP_NAME = "Norman"
    BASE_PATH = "https://www.norman.ai"
    COMPANY_EMAIL = "info@normanbot.com"
    COMPANY_PHONE = "9036671876"
    COMPANY_ADDRESS = "Ilab, Department of Electronics Electrical Engineering, Obafemi Awolowo University, " \
                      "Ile-Ife, Osun State"
    FACEBOOK_SECRET_KEY = "EAAS0PtgoBk4BAElZCZAVTSSvnIbp22YIcWHTZAvbaSvN5TZCud1unGoFDmOaCr6KZCIH72UUGgUO16XQlj7x\
    XVdg9nBv7j6YqpeQ21m6bGASd7idhMHDZBagymIMggstRiheB3SQxjnPD0t9n7tMP872O6Bikny7Ld4DZBie9e3fgZDZD2ddd"


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    # MONGOALCHEMY_DATABASE = "mongodb://lekan:wxPython@ds121980.mlab.com:21980/norman"


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    # Put the db file in project root
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    # MONGO_PORT = 27017
    # MONGO_HOST = "127.0.0.1"
    # MONGOALCHEMY_DATABASE = "norman"


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
    MONGOALCHEMY_DATABASE = "norman"



