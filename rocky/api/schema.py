"""
Michael duPont - michael@mdupont.com
rocky.api.schema
"""

# library
from geoalchemy2 import Geometry
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter
# module
import rocky.models as models
from rocky import db, ma

class BaseSchema(ma.ModelSchema):
    def format(self, obj: object, data: dict) -> dict:
        """Perform any data formatting after dumping the object"""
        return data

    def json(self, obj: object) -> dict:
        """Shortcut for returning JSON-compatible version of an object"""
        data = self.dump(obj).data
        return self.format(obj, data)

class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })

class UserSchema(BaseSchema):
    """Schema for rocky.models.User"""
    class Meta:
        model = models.User
        fields = ('id', 'email')
