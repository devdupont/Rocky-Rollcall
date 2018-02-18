"""
Michael duPont - michael@mdupont.com
rocky.models.cast
"""

# pylint: disable=E1101

# module
from rocky import db
from rocky.models import CRUDMixin

class Cast(CRUDMixin, db.Model):
    """Cast object"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    spoken_as = db.Column(db.String(128), nullable=False)

    description = db.Column(db.String(512))
    show_dates = db.Column(db.String(512))
    url = db.Column(db.String(128))
    
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    venue = db.relationship('Venue', backref=db.backref('casts', lazy='dynamic'))

    def __repr__(self) -> str:
        return '<Cast %r-%s>' % (self.id, self.name)
