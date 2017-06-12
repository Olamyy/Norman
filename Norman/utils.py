# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import hashlib
import json
import os
import random
import string
import uuid
from datetime import datetime, timedelta
from functools import wraps
from threading import Thread
from time import time

from flask import current_app
from flask import flash
from flask import jsonify, make_response
from flask import redirect

from Norman.api.base import base
from Norman.errors import HttpMethodError
from Norman.settings import FBConfig


def async_task(f):
    """ Takes a function and runs it in a thread """
    @wraps(f)
    def _decorated(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return _decorated


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def generate_id(length):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))


def generate_conversation_id(recipient_id):
    chars = recipient_id + str(time())[:5]
    return chars


def hash_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def generate_api_ai_session(data):
    return hash_data(data)[:32]


def validate_hashes(new_password, old):
    return True if hash_data(new_password) == old else False


def generate_session_id():
    return str(uuid.uuid1())


def handle_relative_path(path):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, path)
    return filename


def cookie_insertion(redirect_to, cookie_name, cookie_value):
    redirect_to_index = redirect(redirect_to)
    response = current_app.make_response(redirect_to_index)
    response.set_cookie(cookie_name, cookie_value)
    return response


def last_five_minute():
    return datetime.now() - timedelta(minutes=5)


def decode_data(data):
    return data.decode("utf-8")


def update_white_listed_domains():
    """https://graph.facebook.com/v2.6/me/messenger_profile?access_token=PAGE_ACCESS_TOKEN"""
    graph_api_url = FBConfig.GRAPH_API_URL.replace('messages', 'messenger_profile')
    data = {
        "setting_type": "domain_whitelisting",
        "whitelisted_domains": FBConfig.WHITE_LISTED_DOMAINS,
        "domain_action_type": "add"
            }
    try:
        request = base.exec_request('POST', graph_api_url, data=data)
        return request
    except HttpMethodError:
        return 'Error'


class Response:

    def __init__(self):
        self._response_ok = []
        self._response_error = []

    @staticmethod
    def response_ok(data):
        response = jsonify({'status': 'success', 'data': data}, 200)
        return make_response(response)

    @staticmethod
    def response_error(message, error=None, error_code=None):
        response = json.dumps({'status': 'fail', 'message': message, 'error': error, 'error_code': error_code})
        return make_response(response, 400)

response = Response()

