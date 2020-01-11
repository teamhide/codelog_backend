from marshmallow import Schema, fields, validates, ValidationError


class OAuthLoginRequestSchema(Schema):
    code = fields.String(required=True)

    @validates('code')
    def validate_code(self, data, **kwargs):
        if len(data) == 0:
            raise ValidationError('validation error')


class OAuthLoginResponseSchema(Schema):
    token = fields.String(required=True)
    refresh_token = fields.String(required=True)
    nickname = fields.String(required=True)


class RefreshTokenSchema(Schema):
    token = fields.String(required=True)
    refresh_token = fields.String(required=True)


class VerityTokenRequestSchema(Schema):
    token = fields.String(required=True)
