from typing import List

from flask import jsonify

from app.entities import FeedEntity
from app.schemas import (
    GetFeedListResponseSchema,
    CreateFeedResponseSchema,
    GetTagListResponseSchema
)
from core.presenters import Presenter


class GetFeedListPresenter(Presenter):
    @classmethod
    def transform(cls, response: List[FeedEntity]) -> jsonify:
        for r in response:
            r.nickname = r.user.nickname
        return jsonify(GetFeedListResponseSchema(
            exclude=['is_read'],
        ).dump(response, many=True))


class GetPrivateFeedListPresenter(Presenter):
    @classmethod
    def transform(cls, response: List[FeedEntity]) -> jsonify:
        for r in response:
            r.nickname = r.user.nickname
        return jsonify(GetFeedListResponseSchema().dump(response, many=True))


class CreateFeedPresenter(Presenter):
    @classmethod
    def transform(cls, response: FeedEntity) -> jsonify:
        response.nickname = response.user.nickname
        return jsonify(CreateFeedResponseSchema().dump(response))


class GetTagListPresenter(Presenter):
    @classmethod
    def transform(cls, response) -> jsonify:
        return jsonify(GetTagListResponseSchema().dump(response, many=True))


class SearchFeedPresenter(Presenter):
    @classmethod
    def transform(cls, response: List[FeedEntity]) -> jsonify:
        for r in response:
            r.nickname = r.user.nickname
        return jsonify(GetFeedListResponseSchema().dump(response, many=True))


class DeleteFeedPresenter(Presenter):
    @classmethod
    def transform(cls, response) -> jsonify:
        return jsonify({'status': response})


class ReadFeedPresenter(Presenter):
    @classmethod
    def transform(cls, response):
        return jsonify({'status': response})
