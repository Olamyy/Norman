# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import hashlib
import random
import string
import uuid

from flask import flash
from flask import jsonify, make_response


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


# def sleep_for(duration):
#     time


def validate_hashes(new_password, old):
    return True if hash_data(new_password) == old else False


def generate_session_id():
    return str(uuid.uuid1())


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
        response = jsonify({'status': 'fail', 'message': message, 'error': error})
        return make_response(response, 400)

response = Response()
