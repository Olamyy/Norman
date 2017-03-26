# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from Norman.database import db
from Norman.models import User, Hospital, Service , Plan


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    active = True

    class Meta:
        """Factory configuration."""

        model = User


class HospitalFactory(BaseFactory):
    name = Sequence(lambda n: 'Hospital{0}'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    active = True

    class Meta:
        """Factory configuration."""

        model = Hospital


class ServiceFactory(BaseFactory):
    name = Sequence(lambda n: 'Service{0}'.format(n))
    long_description = Sequence(lambda n: '{0}'.format(n))



