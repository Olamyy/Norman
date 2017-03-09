# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from flask import jsonify


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


class Response:

    def __init__(self):
        self._response_ok = []
        self._response_error = []

    @staticmethod
    def response_ok(data):
        response = {'status': 'success', 'data': data}
        return response

    @staticmethod
    def response_error(message,error):
        response = {'status': 'fail', 'message': message, 'error': error}
        return jsonify(response)

response = Response()
