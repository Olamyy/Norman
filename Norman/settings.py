# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from pymongo import MongoClient


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
    FACEBOOK_SECRET_KEY = 'EAAS0PtgoBk4BAKIZBKELBTB7JZBsoetjvG1A3xmMWhJFlDxeUtfgNgr2odxHZBqZAailae0ev0PaIzLz7ifaWEAfI\
                    KTfWGy35yjejmzA9OJVhH2mxMPNGXzBhE397hWZBJhP8Uz0uJ588lJ4jW5DQN0544Gq1d7BuqYBAxflaiQZDZD'
    GRAPH_API_URL = 'https://graph.facebook.com/v2.6/<action>access_token={0}'.format(FACEBOOK_SECRET_KEY)




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
    MONGODB_DB = 'heroku_qcf3clms'
    MONGODB_HOST = 'ds111559.mlab.com'
    MONGODB_PORT = 11559
    MONGODB_USERNAME = 'Olamilekan'
    MONGODB_PASSWORD = 'toga'
    BASE_URL = 'norman-bot.herokuapp.com/'


class DevConfig(Config, UIConfig, PricingConfig):
    ENV = 'dev'
    DEBUG = True
    # Put the db file in project root
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    MONGODB_DB = 'Norman'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    BASE_URL = "localhost:5000/"
    pymongo_client = MongoClient('mongodb://localhost:27017/')



class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
    MONGOALCHEMY_DATABASE = "norman"
