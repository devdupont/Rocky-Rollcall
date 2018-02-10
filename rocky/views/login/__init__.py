"""
Michael duPont - michael@mdupont.com
rocky.views.login
"""

# pylint: disable=E1101

# stdlib
import json
from datetime import datetime
from urllib.parse import unquote
# library
from flask import flash, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_restful import abort
# module
from rocky import app, db
from rocky.models import User
from rocky.views.login.oauth import OAuthSignIn

lm = LoginManager(app)
lm.login_view = 'login'
lm.login_message = 'Please log in to access this page.'

# def encrypt_param(data: {str: object}, pubkey: str) -> str:
#     """Create a URL-safe, RSA encrypted string from a JSON-compatible object and public key
#     URL-safe means valid alphanumerics and substitutes - instead of + and _ instead of /"""
#     pkobj = RSA.importKey(urlsafe_b64decode(pubkey))
#     edata = pkobj.encrypt(json.dumps(data).encode(), 'x')[0] # the 'x' is ignored
#     return urlsafe_b64encode(edata)
#     # return quote_plus(json.dumps(data))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    rurl = request.args.get('redirect', None)
    session['redirect'] = rurl
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        print('User is anon')
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    userdata = oauth.callback()
    print(userdata)
    if 'social_id' not in userdata:
        print('No social_id')
        return redirect(url_for('login'), 403)
    user = User.query.filter_by(social_id=userdata['social_id']).first()
    print('User', user)
    if not user or not user.is_admin:
        print('Internal not admin')
        return redirect(url_for('login'), 401)
    login_user(user, True)
    print('Redirect to admin portal')
    return redirect('/admin')
