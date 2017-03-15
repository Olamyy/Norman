# -*- coding: utf-8 -*-
"""Hospital models."""
import datetime

from flask_login import UserMixin
from Norman.database import db, PasswordField
from Norman.extensions import bcrypt


class Hospital(UserMixin, db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3)
    password = PasswordField(required=True, max_length=50, min_length=10)
    address = db.StringField(required=True, max_length=1000, min_length=3)
    description = db.StringField(required=True, max_length=1000, min_length=3)
    specialty = db.StringField(required=True, max_length=1000, min_length=3)
    email = db.StringField(required=True, max_length=50, min_length=10)
    image = db.StringField(required=True, max_length=200, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    service_list = db.ListField()
    plan_id = db.StringField(required=True, max_length=200, min_length=3)
    active = db.BooleanField(default=False)

    def __init__(self, password=None):
        """Create instance."""
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
        return '<Hospital({name!r})>'.format(name=self.name)


