"""
Michael duPont - michael@mdupont.com
rocky
"""

# pylint: disable=E1101

# stdlib
from datetime import datetime
# library
from flask import Flask, g, request
from flask_admin import Admin
from flask_cors import CORS
from flask_login import current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Create the web app and add the config data
app = Flask(__name__)
app.config.from_object('config')

# Create the application helper objects
admin = Admin(app, name='Rocky Rollcall', template_mode='bootstrap3')
cors = CORS(app, resources={
    r'/api/*': {'origins': '*'},
    r'/authorize/*': {'origins': '*'},
    r'/callback/*': {'origins': '*'},
    '/login': {'origins': '*'}
})
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from rocky import views, models, api, assistants

@app.before_request
def before_request():
    """Runs before responding to a user request"""
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()