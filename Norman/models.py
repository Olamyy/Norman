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

    def __str__(self):
        pass


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


class Hospital(db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3, unique=True)
    password = db.StringField(required=True, max_length=50, min_length=5)
    address = db.StringField(required=False, max_length=1000, min_length=3)
    description = db.StringField(required=False, max_length=1000, min_length=3)
    specialty = db.StringField(required=False, max_length=1000, min_length=3)
    email = db.StringField(required=True, max_length=50, min_length=10, unique=True)
    image = db.StringField(required=False, max_length=200, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    plan_id = db.StringField(required=True, max_length=200, min_length=3)
    reg_num = db.StringField(required=True, max_length=200, min_length=3, unique=True)
    active = db.BooleanField(default=False)
    ver_id = db.StringField(required=True, max_length=200, min_length=3)
    verificationID = db.StringField(required=True, max_length=4, min_length=4)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Hospital({name!r})>'.format(name=self.name)


class User(UserMixin, db.Document):
    fb_id = db.StringField(max_length=200, min_length=3)
    first_name = db.StringField(required=True, max_length=200, min_length=3)
    user_id = db.StringField(required=True, max_length=20, min_length=3)
    last_name = db.StringField(required=True, max_length=200, min_length=3)
    email = db.EmailField(required=True, max_length=200, min_length=10)
    username = db.StringField(max_length=50, min_length=3)
    hospital_id = db.StringField(required=True, max_length=200, min_length=3)
    services_id = db.StringField(required=True, max_length=200, min_length=3)
    plan_id = db.StringField(required=True, max_length=200, min_length=3)
    is_verified = db.BooleanField(default=False)
    is_on_hospital_list_but_not_on_fb_list = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)
    is_on_plan = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now())

    def __init__(self, **kwargs):
        """Create instance."""
        pass


class Modal(UserMixin, db.Document):

    def __init__(self):
        pass




