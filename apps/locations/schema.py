from marshmallow import fields, ValidationError

from ..utils.base_schema import BaseSchema

from .models import Location


def validate_name(name):
    if City.query.filter_by(name=name).all():
        raise ValidationError(f"City with name '{name}' already exists")


class LocationSchema(BaseSchema):
    name = fields.Str(validate=validate_name)

    class Meta:
        model = Location
