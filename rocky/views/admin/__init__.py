"""
Michael duPont - michael@mdupont.com
rocky.admin
"""

# pylint: disable=E1101

# library
from flask import flash, g, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.geoa import ModelView as GeoModelView
# module
from rocky import admin, db
from rocky.models import User

class AuthModelView(ModelView):
    def is_accessible(self):
        return hasattr(g.user, 'is_admin') and g.user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('Authentication failed.')
        return redirect(url_for('index'))

class AuthGeoModelView(GeoModelView, AuthModelView):
    pass

admin.add_view(AuthModelView(User, db.session, category='User Created'))
