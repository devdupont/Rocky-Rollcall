"""
Michael duPont - michael@mdupont.com
rocky.views
"""

# pylint: disable=E1101

# stdlib
from datetime import datetime
# library
from flask import render_template, g, flash, redirect, url_for, request
from flask_login import login_required, current_user
# module
from rocky import app, db

@app.route('/')
@app.route('/index')
@login_required
def index() -> str:
    return render_template("index.html",
                           title='Home')

@app.errorhandler(401)
def unauthorized_error(error: Exception) -> str:
    db.session.rollback()
    return render_template('error/401.html'), 401

@app.errorhandler(403)
def forbidden_error(error: Exception) -> str:
    db.session.rollback()
    return render_template('error/403.html'), 403

@app.errorhandler(404)
def not_found_error(error: Exception) -> str:
    db.session.rollback()
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(error: Exception) -> str:
    db.session.rollback()
    return render_template('error/500.html'), 500

from rocky.views import admin, login
