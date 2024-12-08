from marshmallow import fields, Schema # type: ignore

class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()
    role = fields.String()

class AnimalSchema(Schema):
    id = fields.String()
    name = fields.String()
    species = fields.String()
    created_at = fields.DateTime()