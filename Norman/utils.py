# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from flask import jsonify, make_response
import string
import random
from bson.json_util import dumps


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def generate_id(length):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))


class Response:

    def __init__(self):
        self._response_ok = []
        self._response_error = []

    @staticmethod
    def response_ok(data):
        try:
            oid = data._id
            data._id = str(oid)
        except AttributeError:
            pass
        try:
            oid = data['_id']
            data['_id'] = str(oid)
        except KeyError:
            pass


        response = jsonify({'status': 'success', 'data': data}, 200)
        return make_response(response)

    @staticmethod
    def response_error(message, error=None):
        response = jsonify({'status': 'fail', 'message': message, 'error': error})
        return make_response(response)

response = Response()
