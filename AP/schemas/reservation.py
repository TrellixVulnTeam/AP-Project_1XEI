from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

from schemas.user import UserSchema
from models.workspace import Workspace


class ReservationSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    reservor = fields.Nested(UserSchema, attribute='user', dump_only=True, only='name')
    datetime = fields.DateTime(dump_only=True)
    datetimeend = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    workspace = fields.Method(required=True, deserialize='get_workspace')

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kargs):
        if many:
            return {'data': data}
        return data

    @validates('datetime')
    def validate_datetime(self, value):
        if value < "13:00:00":
            raise ValidationError('Reservation start must be after 13:00:00')

    def get_workspace(self, value):
        return Workspace.get_by_name(value).id
