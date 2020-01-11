from marshmallow import Schema, fields, validates, ValidationError


class GetFeedListResponseSchema(Schema):
    id = fields.Integer(required=True)
    nickname = fields.String(required=True)
    image = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    url = fields.String(required=True)
    tags = fields.List(fields.Str)
    created_at = fields.String()
    updated_at = fields.String()


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
