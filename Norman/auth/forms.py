from flask_wtf import Form
from mongoengine import DoesNotExist
from wtforms import PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired
from Norman.models import Hospital
from Norman.utils import hash_data


class LoginForm(Form):
    """Login form."""

    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember', validators=[])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        password = hash_data(self.password.data)
        try:
            self.user = Hospital.objects.get(email=self.email.data, password=password)
            return self.user
        except DoesNotExist:
                return False

class PatientLoginForm(Form):
    """Login form."""

    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember', validators=[])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PatientLoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(PatientLoginForm, self).validate()
        if not initial_validation:
            return False

        password = hash_data(self.password.data)
        try:
            self.user = Hospital.objects.get(email=self.email.data, password=password)
            return self.user
        except DoesNotExist:
                return False

class PatientPasswordChooseForm(Form):
    """Login form."""

    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember', validators=[])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PatientPasswordChooseForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(PatientPasswordChooseForm, self).validate()
        if not initial_validation:
            return False

        password = hash_data(self.password.data)
        try:
            self.user = Hospital.objects.get(email=self.email.data, password=password)
            return self.user
        except DoesNotExist:
                return False

class VerificationForm(Form):
    """
    Verification Specific Form
    """
    verficationID = StringField('email', validators=[DataRequired()])
