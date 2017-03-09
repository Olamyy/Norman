from .compat import basestring
from .extensions import db

from mongoalchemy.py3compat import *
from mongoalchemy.fields import StringField


class PasswordField(StringField):
    '''
    Unicode Strings.  ``unicode`` is used to wrap and unwrap values,
        and any subclass of basestring is an acceptable input
        '''

    def __init__(self, max_length=None, min_length=None, **kwargs):
        ''' :param max_length: maximum string length
            :param min_length: minimum string length
            :param kwargs: arguments for :class:`Field`
        '''

        self.max = max_length
        self.min = min_length
        super(StringField, self).__init__(constructor=unicode, **kwargs)

    def validate_wrap(self, value):
        '''
        Validates the type and length of ``value``
        '''
        if not isinstance(value, basestring):
            self._fail_validation_type(value, basestring)
        if self.max is not None and len(value) > self.max:
            self._fail_validation(value, 'Value too long (%d)' % len(value))
        if self.min is not None and len(value) < self.min:
            self._fail_validation(value, 'Value too short (%d)' % len(value))