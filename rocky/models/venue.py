"""
Michael duPont - michael@mdupont.com
timevite.models.city
"""

# pylint: disable=E1101

# library
import shapely
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
# module
from rocky import db
from rocky.models import CRUDMixin

class Venue(CRUDMixin, db.Model):
    """Venue object"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128))
    state = db.Column(db.String(128))
    city = db.Column(db.String(128))
    address = db.Column(db.String(256))
    zip = db.Column(db.Integer)
    geom = db.Column(Geometry('POINT'))
    # casts : backref from cast.Cast

    @property
    def as_shape(self) -> str:
        """The geometry as a shapely geometry"""
        return to_shape(self.geom)

    @property
    def geom_raw(self) -> str:
        """Returns the raw GIS geometry string"""
        return shapely.wkt.dumps(self.as_shape)

    # def set_geom(self, geom: [[float]]):
    #     """Set the venue's boundary geometry from a list of coordinate pairs"""
    #     self.geom = from_shape(shapely.geometry.Point(geom))

    # def get_geom(self) -> [[float]]:
    #     """Returns the city's boundary geometry"""
    #     return list(self.as_shape.exterior.coords)

    def __repr__(self) -> str:
        return f'<Venue {self.city}-{self.name}>'
