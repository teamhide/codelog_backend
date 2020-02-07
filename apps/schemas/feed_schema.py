from datetime import timedelta

from marshmallow import Schema, fields, validates, ValidationError


class GetFeedListResponseSchema(Schema):
    id = fields.Integer(required=True)
    nickname = fields.String(required=True)
    image = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    url = fields.String(required=True)
    tags = fields.List(fields.Str)
    is_read = fields.Boolean(required=True)
    created_at = fields.Method('get_created_at')
    updated_at = fields.Method('get_updated_at')

    def get_created_at(self, obj):
        return str((obj.created_at + timedelta(hours=9)).replace(microsecond=0))

    def get_updated_at(self, obj):
        return str((obj.updated_at + timedelta(hours=9)).replace(microsecond=0))


class CreateFeedRequestSchema(Schema):
    url = fields.String(required=True)
    tags = fields.String(required=True)
    is_private = fields.String(required=True)


class CreateFeedResponseSchema(Schema):
    id = fields.Integer(required=True)
    nickname = fields.String(required=True)
    image = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    url = fields.String(required=True)
    tags = fields.List(fields.Str)
    created_at = fields.String()
    updated_at = fields.String()


class GetTagListResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)


class SearchFeedRequestSchema(Schema):
    keyword = fields.String(required=True)
    prev = fields.Integer(required=False)

    @validates('keyword')
    def validate_keyword(self, data, **kwargs):
        if len(data) <= 1:
            raise ValidationError('validation error')
