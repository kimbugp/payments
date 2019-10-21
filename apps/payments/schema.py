from marshmallow import ValidationError, fields

from ..utils.base_schema import BaseSchema
from .models import Payments


class PaymentsSchema(BaseSchema):
    class Meta:
        model = Payments
