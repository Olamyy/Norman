# -*- coding: utf-8 -*-
"""Hospital models."""
import datetime

from flask_login import UserMixin
from Norman.database import db, PasswordField
from Norman.utils import generate_id


class Hospital(UserMixin, db.Document):
    hospital_id = db.ObjectIdField()
    # hospital_id = db.StringField(required=True, max_length=200, min_length=3)
    name = db.StringField(required=True, max_length=200, min_length=3)
    password = PasswordField(max_length=100, min_length=10)
    address = db.StringField(required=True, max_length=1000, min_length=3)
    description = db.StringField(required=True, max_length=1000, min_length=3)
    specialty = db.StringField(required=True, max_length=1000, min_length=3)
    email = db.StringField(required=True, max_length=50, min_length=10)
    image = db.StringField(required=False, max_length=200, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    plan_id = db.StringField(required=True, max_length=200, min_length=3)
    active = db.BooleanField(default=False)


