# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get('NORMAN_SECRET', 'a9fb1b64-1f0f-11e7-95e2-7077816bf77d')  # TODO: Change me
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


class ApiAIConfig:
    CLIENT_ACCESS_TOKEN = '223fceac22164b419316b65979d86fdb'
    DEVELOPER_ACCESS_TOKEN = '0796bc4020714af4a4d91255a31d5f33'


class UIConfig:
    APP_NAME = "Norman"
    BASE_PATH = "https://www.norman.ai"
    COMPANY_EMAIL = "info@normanbot.com"
    COMPANY_PHONE = "9036671876"
    COMPANY_ADDRESS = "Ilab, Department of Electronics Electrical Engineering, Obafemi Awolowo University, " \
                      "Ile-Ife, Osun State"

    NORMAN_FEATURES_LEFT = {"Your Data In Cloud": "Norman seamlessly syncs your patient data between\
                                their social media account and your hospital portal",
                            "Security": "The core Norman philosophy is security.\
                                Norman keeps whatever data its getting, retrieving and saving between you and your\
                            patients completely secure.",
                            "AI inspired Design": "Norman was designed with a core AI enabled technology."
                                                  "As such, it has been designed to converse with your \
                            patients in all the standard medical ways.",
                            }
    NORMAN_FEATURES_RIGHT = {"Human Readable Data Format": "Every data collected by Norman about\
                                your patient is formatted in a well structured human readable table.",

                             "Excellent Performance": "Norman has a 100% response rate and as such\
                                is always there for your patients..",

                             "Machine Learning": "Norman uses machine learning to continuously learn from each\
                                conversation it has with your patient. As such, it provides better, faster help everytime.",
                             }


class ProdConfig(Config, UIConfig):
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


class DevConfig(Config, UIConfig):
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


class ErrorConfig(Config):
    INVALID_VER_ID_ERROR = "Invalid/Expired Verification ID"
    INVALID_ROUTE_ERROR = "Looks like you do not have access to this page."
    INVALID_LOGIN_ERROR = "Invalid Email or Password"


class MessageConfig(Config):
    GET_STARTED_MESSAGE = "Hello <username>, My name is {0}. I am medical assistance " \
                          "bot that helps you keep track of your health while syncing it " \
                          "seamlessly with your hospital.".format(UIConfig.APP_NAME)
    GET_STARTED_MEANING = "It means I help you keep track of vital personal health information. " \
                          "I then update your hospital with this information to help you treat you better"
    GET_STARTED_HOW = "I do this by asking you some questions overtime. I also carry out some of the services your " \
                      "hospitals assigns me to monitor on you."
    GET_STARTED_SERVICE_LIST = ""
    GET_HELP_MESSAGE = ""


class MailConfig(Config):
    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'olamyy53@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'haleeyah')

    # administrator list
    ADMINS = "olamyy53@gmail.com"