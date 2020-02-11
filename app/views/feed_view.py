from typing import NoReturn, Union

from flask import Blueprint, request, jsonify
from marshmallow.exceptions import ValidationError

from app.presenters import (
    GetFeedListPresenter,
    GetPrivateFeedListPresenter,
    CreateFeedPresenter,
    GetTagListPresenter,
    SearchFeedPresenter,
    DeleteFeedPresenter,
    ReadFeedPresenter,
)
from app.schemas import CreateFeedRequestSchema, SearchFeedRequestSchema
from app.usecases import (
    GetFeedListUsecase,
    CreateFeedUsecase,
    GetTagListUsecase,
    SearchFeedUsecase,
    DeleteFeedUsecase,
    ReadFeedUsecase,
)
from core.decorators import is_jwt_authenticated
from core.exceptions import abort

feed_bp = Blueprint('feeds', __name__, url_prefix='/api/feeds')


@feed_bp.route('/', methods=['GET'])
def get_feed_list() -> Union[NoReturn, jsonify]:
    header = request.headers.get('Authorization')
    feeds = GetFeedListUsecase().execute(
        header=header,
        prev=request.args.get('prev'),
    )
    return GetFeedListPresenter.transform(response=feeds)


@feed_bp.route('/private', methods=['GET'])
def get_private_feed_list() -> Union[NoReturn, jsonify]:
    header = request.headers.get('Authorization')
    feeds = GetFeedListUsecase().execute(
        header=header,
        prev=request.args.get('prev'),
    )
    return GetPrivateFeedListPresenter.transform(response=feeds)


@feed_bp.route('/', methods=['POST'])
@is_jwt_authenticated()
def create_feed(payload: dict) -> Union[NoReturn, jsonify]:
    try:
        validator = CreateFeedRequestSchema().load(data=request.form)
    except ValidationError:
        abort(400, error='validation error')

    feed = CreateFeedUsecase().execute(**validator, payload=payload)
    return CreateFeedPresenter.transform(response=feed)


@feed_bp.route('/tags/', methods=['GET'])
def get_tag_list() -> Union[NoReturn, jsonify]:
    tags = GetTagListUsecase().execute()
    return GetTagListPresenter().transform(response=tags)


@feed_bp.route('/search', methods=['GET'])
def search_feed() -> Union[NoReturn, jsonify]:
    try:
        validator = SearchFeedRequestSchema().load(data=request.args)
    except ValidationError:
        abort(400, error='validation error')

    header = request.headers.get('Authorization')
    feeds = SearchFeedUsecase().execute(**validator, header=header)
    return SearchFeedPresenter.transform(response=feeds)


@feed_bp.route('/<int:feed_id>', methods=['DELETE'])
@is_jwt_authenticated()
def delete_feed(payload: dict, feed_id: int) -> Union[NoReturn, jsonify]:
    response = DeleteFeedUsecase().execute(payload=payload, feed_id=feed_id)
    return DeleteFeedPresenter.transform(response=response)


@feed_bp.route('/<int:feed_id>/read', methods=['GET'])
@is_jwt_authenticated()
def read_feed(payload: dict, feed_id: int) -> Union[NoReturn, jsonify]:
    response = ReadFeedUsecase().execute(payload=payload, feed_id=feed_id)
    return ReadFeedPresenter.transform(response=response)
