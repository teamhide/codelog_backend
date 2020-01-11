from typing import NoReturn, Union

from flask import Blueprint, request, jsonify
from marshmallow.exceptions import ValidationError

from apps.presenters import (
    GetFeedListPresenter,
    CreateFeedPresenter,
    GetTagListPresenter,
    SearchFeedPresenter,
    DeleteFeedPresenter,
)
from apps.schemas import CreateFeedRequestSchema, SearchFeedRequestSchema
from apps.usecases import (
    GetFeedListUsecase,
    CreateFeedUsecase,
    GetTagListUsecase,
    SearchFeedUsecase,
    DeleteFeedUsecase,
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
