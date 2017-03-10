import datetime

from flask_login import UserMixin
from Norman.database import db, PasswordField
from Norman.extensions import bcrypt


class Hospital(UserMixin, db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3)
    fb_id = db.StringField(max_length=200, min_length=3)
    first_name = db.StringField(required=True, max_length=200, min_length=3)
    last_name = db.StringField(required=True, max_length=200, min_length=3)
    email = db.EmailField(required=True, max_length=200, min_length=10)
    username = db.StringField(required=True, max_length=50, min_length=3)
    hospital_id = db.StringField(required=True, max_length=200, min_length=3)
    services_id = db.StringField(required=True, max_length=200, min_length=3)
    plan_id = db.StringField(required=True, max_length=200, min_length=3)
    password = PasswordField(required=True, max_length=50, min_length=10)
    is_verified = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now())

    def __init__(self, name, email, password=None, **kwargs):
        """Create instance."""
        db.Document.__init__(self, name=name, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Norman User({name!r})>'.format(name=self.name)


