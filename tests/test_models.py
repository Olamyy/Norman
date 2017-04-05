# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from Norman.models import User, Hospital

from .factories import UserFactory



@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""
    def __int__(self):
        self.user = User(first_name='foo', last_name='bar', emai='foo@bar.com', hospital_id='hospital_id',
                services_id='services', plan_id='plan_id')

    def test_get_by_id(self):
        """Get user by ID."""
        self.user.save()

        retrieved = User.get_by_id(self.user.id)
        assert retrieved == self.user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        self.user.save()
        assert bool(self.user.created_at)
        assert isinstance(self.user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        self.user.save()
        assert self.user.password is None

    def test_factory(self, db):
        """Test user factory."""
        self.user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(self.user.username)
        assert bool(self.user.email)
        assert bool(self.user.created_at)
        assert self.user.is_admin is False
        assert self.user.active is True
        assert self.user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert self.user.check_password('foobarbaz123') is True
        assert self.user.check_password('barfoobaz') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'


@pytest.mark.usefixtures('db')
class TestHospital:
    def __int__(self):
        self.user = Hospital(first_name='foo', last_name='bar', emai='foo@bar.com', hospital_id='hospital_id',
                             services_id='services', plan_id='plan_id')
