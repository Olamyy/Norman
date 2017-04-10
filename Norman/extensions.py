# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_restful import Api
from flask_mail import Mail

csrf_protect = CSRFProtect()
db = MongoEngine()
migrate = Migrate()
api = Api()
session_interface = MongoEngineSessionInterface(db)
cache = Cache()
debug_toolbar = DebugToolbarExtension()
mailer = Mail()
