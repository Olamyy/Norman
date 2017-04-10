# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get('NORMAN_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    __version__ = '0.0.1'
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Di-sable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGOALCHEMY_DATABASE = "norman"


class FBConfig(Config):
    """
    The GRAPH_API_URL format is <base_url><version><action><fields>
    """
    FACEBOOK_SECRET_KEY = 'EAAS0PtgoBk4BAKIZBKELBTB7JZBsoetjvG1A3xmMWhJFlDxeUtfgNgr2odxHZBqZAailae0ev0PaIzLz7ifaWEAfIKTfWGy35yjejmzA9OJVhH2mxMPNGXzBhE397hWZBJhP8Uz0uJ588lJ4jW5DQN0544Gq1d7BuqYBAxflaiQZDZD'
    GRAPH_API_VERSION = 'v2.6'
    GRAPH_API_URL = 'https://graph.facebook.com/{0}/me/messages?access_token={1}'.format(
        GRAPH_API_VERSION, FACEBOOK_SECRET_KEY)


class UIConfig:
    APP_NAME = "Norman"
    BASE_PATH = "https://www.norman.ai"
    COMPANY_EMAIL = "info@normanbot.com"
    COMPANY_PHONE = "9036671876"
    COMPANY_ADDRESS = "Ilab, Department of Electronics Electrical Engineering, Obafemi Awolowo University, "\
                      "Ile-Ife, Osun State"

    NORMAN_FEATURES_TEXT = {"feature1": "feature1desc",
                            "feature2": "feature2desc",
                            "feature3": "feature2desc",
                            "feature4": "feature2desc",
                            "feature5": "feature2desc",
                            "feature6": "feature2desc"
                            }

    # @Todo:Stats format would be a dict of the format {stats:{"value":value, "text":text}}
    NORMAN_STATS = {

                    }
    NORMAN_DEMO_VIDEO_TEXT = """Watch a quick short video explaining the ideology behind Norman.\n
                                It demonstrates how Norman works and how you can use it.""".replace('\n', '<br />')
    # @Todo:FAQ format would be a dict of the format {faq_short_description:answer}
    # NORMAN_FAQ_TEXT = {}


class PricingConfig:
    pass


class ProdConfig(Config, UIConfig, PricingConfig):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    BASE_URL = 'norman-bot.herokuapp.com/'
    MONGODB_SETTINGS = {
        'db': 'heroku_qcf3clms',
        'host': 'ds111559.mlab.com',
        'port': 11559,
        'username': 'Olamilekan',
        'password': 'toga',
        'alias': 'default'
    }


class DevConfig(Config, UIConfig, PricingConfig):
    ENV = 'dev'
    DEBUG = True
    # Put the db file in project root
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    MONGODB_SETTINGS = {
        'db': 'Norman',
        'host': '127.0.0.1',
        'port': 27017,
        'password': 'toga',
        'alias': 'default'
    }


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
    MONGOALCHEMY_DATABASE = "norman"


class MailerConfig(Config):
    MAIL_SERVER = ''
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False


class ErrorConfig(Config):
    INVALID_LOGIN_ERROR = "Invalid Email or Password"
