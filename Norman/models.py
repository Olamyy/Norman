# -*- coding: utf-8 -*-
"""Custom Models."""
import datetime

from flask_login import UserMixin
from Norman.database import db


class Service(UserMixin, db.Document):
    name = db.StringField(required=True, max_length=200, min_length=3)
    description = db.StringField(required=True, max_length=200, min_length=3)
    service_hash_desc = db.StringField(required=True, max_length=200, min_length=3)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    # service_fee = db.S

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Service({name!r})>'.format(name=self.name)
