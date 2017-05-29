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

class GoogleConfig(Config):
    PLACES_API_KEY = 'AIzaSyAmoOVSZfK0Av6j_ONXa343qyYLGVczlS4'

class FBConfig(Config):
    """
    The GRAPH_API_URL format is <base_url><version><action><fields>
    """
    FACEBOOK_SECRET_KEY = 'EAAS0PtgoBk4BAKIZBKELBTB7JZBsoetjvG1A3xmMWhJFlDxeUtfgNgr2odxHZBqZAailae0ev0PaIzLz7ifaWEAfIKTfWGy35yjejmzA9OJVhH2mxMPNGXzBhE397hWZBJhP8Uz0uJ588lJ4jW5DQN0544Gq1d7BuqYBAxflaiQZDZD'
    GRAPH_API_VERSION = 'v2.6'
    GRAPH_API_URL = 'https://graph.facebook.com/{0}/me/messages?access_token={1}'.format(
        GRAPH_API_VERSION, FACEBOOK_SECRET_KEY)
    WHITE_LISTED_DOMAINS = [
        "https://wallpaperbrowse.com/media/images/pictures-14.jpg",
        "http://norman-bot.herokuapp.com/static/landing/images/norman-android.png"
    ]

class ApiAIConfig:
    CLIENT_ACCESS_TOKEN = '223fceac22164b419316b65979d86fdb'
    DEVELOPER_ACCESS_TOKEN = '0796bc4020714af4a4d91255a31d5f33'


class UIConfig:
    APP_NAME = "Norman"
    BASE_PATH = "https://www.norman-bot.herokuapp.com"
    COMPANY_EMAIL = "bot.normanai@gmail.com"
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
    SERVICE_URL = 'norman-bot.herokuapp.com/services/'
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


class MailerConfig(Config):
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = None
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False
    ADMINS = ['davash001@gmail.com']


class ErrorConfig(Config):
    INVALID_VER_ID_ERROR = "Invalid/Expired Verification ID"
    INVALID_ROUTE_ERROR = "Looks like you do not have access to this page."
    INVALID_LOGIN_ERROR = "Invalid Email or Password"
    INVALID_ID_ERROR = "The provided ID is invalid"
    UNABLE_TO_SET_PASSWORD_ERROR = "Unable to set the provided password"

    @classmethod
    def get_error_by_code(cls, error_code):
        error_dict = {'invalidRoute': 'Looks like you do not have access to this page.',
                      'somethingWrong': 'Ooops. Something wrong happened.',
                      'UnableToSetPassword': 'Unable to set the provided password'
                      }
        return [message for action, message in error_dict.items() if action == error_code]


class MessageConfig(Config):
    GET_ALL_SERVICE_LIST = "Hi <username>, you can go to {0} anytime to view a list of all the services I offer".format(
        ProdConfig.SERVICE_URL)
    GET_STARTED_MESSAGE = "Hello <username>, My name is {0}. I am Medical Assistance " \
                          "Bot that helps you keep track of your health while syncing it " \
                          "seamlessly with your hospital.".format(UIConfig.APP_NAME)
    GET_STARTED_MEANING = "It means I help you keep track of vital personal health information. " \
                          "I then update your hospital with this information to help treat you better"
    GET_STARTED_HOW = "I do this by asking you some questions overtime. I also carry out some of the services your " \
                      "hospitals assigns me to on you."
    GET_HELP_MESSAGE = "Hi <username>, what do you need help with?"

    COMING_FROM_HOSPITAL = "Great. I can see you have been brought here from your hospital dashboard."

    EMOJI_DICT = {'HAPPY_SMILE': '😊', 'BOWING_MAN': '🙇'}

    TIME_TO_SET_UP = "Please {0}, give me some minutes to get you all set up. I promise I won't take long.".format(
        EMOJI_DICT['BOWING_MAN'])

    FIRST_TIME_TEMP_USER = ["You are currently using me as a free user."]


class RegexConfig(Config):
    BotInfoMatcher = ['what [is|are|will|was]+\ your name', 'VP+ *+ your name',
                      'who [is|are|will|was]+\ your creator|dad|mom|father|mother|papa|mama|daddy|mommy',
                      'VP+ *+ your creator|dad|mom|father|mother', 'who [made|created|wrote|built]+\ you']
    GreetingsMatcher = ['hi', 'hey', 'hello', 'greetings', 'good morning', 'good afternoon', 'good evening', 'bawo']

    ByeMatcher = ['bye', 'see you']
    MessagingServiceMatcher = ['leave a message [for|to]+\ \w [that|saying|] I will be home']


class YelpConfig(Config):
    YELP_V3_TOKEN = None
    CONSUMER_KEY = None
    CONSUMER_SECRET = None
    TOKEN = None
    TOKEN_SECRET = None


class ServiceListConfig(Config):
    messaging = {
        "title": "Real-Time Messaging",
        "image_url": "https://norman-bot.herokuapp.com/static/landing/images/norman-android.png",
        "subtitle": "Real-time messaging interface between medical assistance bot and you",
        "default_action": {
            "type": "web_url",
            "url": "https://norman-bot.herokuapp.com/services",
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": "https://norman-bot.herokuapp.com/"
        },
        "buttons": [
            {
                "title": "Read More",
                "type": "web_url",
                "url": "https://norman-bot.herokuapp.com/services",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://norman-bot.herokuapp.com/"
            }
        ]
    }

    reminder = {
        "title": "Reminder",
        "image_url": "https://norman-bot.herokuapp.com/static/landing/images/a.png",
        "subtitle": "The bot handles Drug use reminder,Appointment reminders and Some User Specific Reminders",
        "default_action": {
            "type": "web_url",
            "url": "https://norman-bot.herokuapp.com/services",
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": "https://norman-bot.herokuapp.com/"
        },
        "buttons": [
            {
                "title": "Read More",
                "type": "web_url",
                "url": "https://norman-bot.herokuapp.com/services",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://norman-bot.herokuapp.com/"
            }
        ]
    }

    scheduling = {
        "title": "Appointment/Scheduling",
        "image_url": "https://norman-bot.herokuapp.com/static/landing/images/b.png",
        "subtitle": "This service allows patients to fix appointment at hospital.",
        "default_action": {
            "type": "web_url",
            "url": "https://norman-bot.herokuapp.com/services",
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": "https://norman-bot.herokuapp.com/"
        },
        "buttons": [
            {
                "title": "Read More",
                "type": "web_url",
                "url": "https://norman-bot.herokuapp.com/services",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://norman-bot.herokuapp.com/"
            }
        ]
    }

    emergency = {
        "title": "Emergency",
        "image_url": "https://norman-bot.herokuapp.com/static/landing/images/c.png",
        "subtitle": "The emergency service handles all emergency related activities.",
        "default_action": {
            "type": "web_url",
            "url": "https://norman-bot.herokuapp.com/services",
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": "https://norman-bot.herokuapp.com/"
        },
        "buttons": [
            {
                "title": "Read More",
                "type": "web_url",
                "url": "https://norman-bot.herokuapp.com/services",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://norman-bot.herokuapp.com/"
            }
        ]
    }
