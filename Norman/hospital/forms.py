# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, TextAreaField, TextField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import Hospital


class RegisterForm(Form):
    """Register form."""

    name = StringField('Name',
                       validators=[DataRequired(), Length(min=3, max=200)])
    address = TextAreaField('Address',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        hospital = Hospital.query.filter_by(name=self.name.data).first()
        print('I got here')
        print(hospital)
        if hospital:
            self.name.errors.append('Name already registered')
            return False
        hospital = Hospital.query.filter_by(email=self.email.data).first()
        if hospital:
            self.email.errors.append('Email already registered')
            return False
        return True
