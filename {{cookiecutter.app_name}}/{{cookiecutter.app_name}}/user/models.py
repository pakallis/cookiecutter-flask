# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from mongoengine import Document
from flask_login import UserMixin

from {{cookiecutter.app_name}}.database import db
from {{cookiecutter.app_name}}.extensions import bcrypt


class Role(Document):
    """A role for a user."""

    name = StringField(required=True, unique=True)
    user_id = ReferenceField(User)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(Document):
    """A user of the app."""
    username = StringField(unique=True, required=True)
    email = StringField(unique=True, required=True)
    #: The hashed password
    password = BinaryField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.utcnow)
    first_name = StringField(db.String(30), required=True)
    last_name = StringField(required=True)
    active = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    roles = ListField(ReferenceField(User))

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
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

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
