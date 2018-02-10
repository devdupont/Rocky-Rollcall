"""
Michael duPont - michael@mdupont.com
rocky.models.user
"""

# pylint: disable=E1101

# stdlib
import re
# library
from flask_login import UserMixin
# module
from rocky import db
from rocky.models import CRUDMixin

class User(UserMixin, CRUDMixin, db.Model):
    """User object"""
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def __repr__(self) -> str:
        return '<User %r-%s>' % (self.id, self.email)
