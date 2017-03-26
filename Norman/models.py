# -*- coding: utf-8 -*-
"""Custom Models."""
import datetime
from flask_login import UserMixin
from Norman.database import db


class Service(db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3, unique=True)
    long_description = db.StringField(required=True, max_length=1000, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    short_description = db.StringField(required=True, max_length=200, min_length=3)
    service_id = db.StringField(required=True, max_length=1000, min_length=3)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Service({name!r})>'.format(name=self.name)


class Plan(db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3)
    short_description = db.StringField(required=True, max_length=200, min_length=3)
    long_description = db.StringField(required=True, max_length=1000, min_length=3)
    plan_hashed = db.StringField(required=True, max_length=200, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    services_in_plan = db.ListField(max_entries=10)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Plan({name!r})>'.format(name=self.name)


class Hospital(UserMixin, db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3)
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


class User(UserMixin, db.Document):
    fb_id = db.StringField(max_length=200, min_length=3)
    first_name = db.StringField(required=True, max_length=200, min_length=3)
    user_id = db.StringField(required=True, max_length=20, min_length=3)
    last_name = db.StringField(required=True, max_length=200, min_length=3)
    email = db.EmailField(required=True, max_length=200, min_length=10)
    username = db.StringField(required=True, max_length=50, min_length=3)
    hospital_id = db.StringField(required=True, max_length=200, min_length=3)
    services_id = db.StringField(required=True, max_length=200, min_length=3)
    plan_id = db.StringField(required=True, max_length=200, min_length=3)
    is_verified = db.BooleanField(default=False)
    is_on_hospital_list_but_not_on_fb_list = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)
    is_on_plan = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now())




