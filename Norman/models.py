# -*- coding: utf-8 -*-
"""Custom Models."""
import datetime

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
    password = db.StringField(required=True, max_length=200, min_length=5)
    address = db.StringField(required=False, max_length=1000, min_length=3)
    description = db.StringField(required=False, max_length=1000, min_length=3)
    specialty = db.StringField(required=False, max_length=1000, min_length=3)
    email = db.StringField(required=True, max_length=50, min_length=10, unique=True)
    image = db.StringField(required=False, max_length=200, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    plan_id = db.StringField(required=True, max_length=200, min_length=3)
    reg_num = db.StringField(required=True, max_length=200, min_length=3, unique=True)
    active = db.BooleanField(default=False)
    tempID = db.StringField(required=True, max_length=200, min_length=3)
    verificationID = db.StringField(required=True, max_length=4, min_length=4)
    is_logged_in = db.BooleanField(default=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Hospital({name!r})>'.format(name=self.name)


class UserModel(db.Document):
    username = db.StringField(required=True, max_length=200, min_length=3)
    first_name = db.StringField(max_length=200, min_length=3)
    last_name = db.StringField(max_length=200, min_length=3)
    user_id = db.StringField(max_length=20, min_length=3)
    fb_id = db.StringField(max_length=200, min_length=3)
    hospital_id = db.StringField(max_length=200, min_length=3)
    email = db.EmailField(max_length=200, min_length=10)
    plan_id = db.StringField(max_length=200, min_length=3)
    is_verified = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)
    is_on_plan = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    session_ids = db.ListField()
    has_sent_first_message = db.BooleanField(default=False)


class Conversation(db.Document):
    fb_id = db.StringField(max_length=200, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    is_alive = db.BooleanField(default=True)
    last_message = db.StringField(max_length=200, min_length=3)


class Session(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now())
    message_count = db.IntField()
    session_id = db.StringField(required=True, max_length=200, min_length=3)




