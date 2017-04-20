# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import hashlib
import json
import os
import random
import string
import uuid

from flask import current_app
from flask import flash
from flask import jsonify, make_response
from flask import redirect


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def generate_id(length):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))


def hash_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


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


class Response:

    def __init__(self):
        self._response_ok = []
        self._response_error = []

    @staticmethod
    def response_ok(data):
        response = jsonify({'status': 'success', 'data': data}, 201)
        return make_response(response)

    @staticmethod
    def response_error(message, error=None):
        response = json.dumps({'status': 'fail', 'message': message, 'error': error})
        return make_response(response, 400)

response = Response()
