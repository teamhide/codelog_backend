from datetime import datetime
from unittest.mock import patch

import pytest
from werkzeug.exceptions import HTTPException

from apps.entities import FeedEntity, UserEntity, TagEntity
from apps.usecases import (
    GetFeedListUsecase,
    CreateFeedUsecase,
    OGTag,
    GetTagListUsecase,
    SearchFeedUsecase,
    DeleteFeedUsecase,
    ReadFeedUsecase,
)

header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.Z7kKIXJIcvElYY7PMM7wx8qe43GAbTADYOct5eqEseA'


@patch('apps.repositories.FeedMySQLRepo.get_feed_list')
def test_get_feed_list_usecase(get_feed_list):
    get_feed_list.return_value = [FeedEntity()]
    feeds = GetFeedListUsecase().execute(
        header=header,
    )
    assert type(feeds) == list
    assert isinstance(feeds[0], FeedEntity)


@patch('apps.repositories.UserMySQLRepo.get_user')
@patch('apps.usecases.CreateFeedUsecase._parse')
@patch('apps.repositories.FeedMySQLRepo.create_feed')
@patch('apps.repositories.FeedMySQLRepo.get_recent_feeds')
def test_create_feed_usecase(get_recent_feeds, create_feed, _parse, get_user):
    get_recent_feeds.return_value = []
    _parse.return_value = OGTag(
        title='test title',
        image='test image',
        description='test description',
    )
    # Case of user is None
    get_user.return_value = None
    with pytest.raises(HTTPException):
        CreateFeedUsecase().execute(
            url='https://hides.kr',
            tags='python, golang',
            is_private='true',
            payload={'user_id': 1}
        )

    # Case of invalid tags
    get_user.return_value = UserEntity(id=1)
    with pytest.raises(HTTPException):
        CreateFeedUsecase().execute(
            url='https://hides.kr',
            tags='#pythonpythonpythonpythonpythonpython',
            is_private='true',
            payload={'user_id': 1}
        )

    # Case of spam
    get_recent_feeds.return_value = [
        FeedEntity(created_at=datetime.now()),
        FeedEntity(),
        FeedEntity(),
    ]
    with pytest.raises(HTTPException):
        CreateFeedUsecase().execute(
            url='https://hides.kr',
            tags='#pythonpythonpythonpythonpythonpython',
            is_private='true',
            payload={'user_id': 1}
        )

    # Case of success
    get_recent_feeds.return_value = []
    create_feed.return_value = FeedEntity()
    feed = CreateFeedUsecase().execute(
            url='https://hides.kr',
            tags='#python',
            is_private='true',
            payload={'user_id': 1}
        )
    assert isinstance(feed, FeedEntity)


@patch('apps.repositories.FeedMySQLRepo.get_tag_list')
def test_get_tag_list_usecase(get_tag_list):
    get_tag_list.return_value = [TagEntity()]
    tags = GetTagListUsecase().execute()
    assert type(tags) == list
    assert isinstance(tags[0], TagEntity)


@patch('apps.repositories.FeedMySQLRepo.search_feed')
def test_search_feed_usecase(search_feed):
    search_feed.return_value = [FeedEntity()]
    feeds = SearchFeedUsecase().execute(
        header=header,
        keyword='test',
    )
    assert type(feeds) == list
    assert isinstance(feeds[0], FeedEntity)


@patch('apps.repositories.UserMySQLRepo.get_user')
@patch('apps.repositories.FeedMySQLRepo.get_feed')
@patch('apps.repositories.FeedMySQLRepo.delete_feed')
def test_delete_feed_usecase(delete_feed, get_feed, get_user):
    # Case of user is None
    get_user.return_value = None
    with pytest.raises(HTTPException):
        DeleteFeedUsecase().execute(payload={'user_id': 1}, feed_id=1)

    # Case of permission denied
    get_user.return_value = UserEntity(id=1)
    get_feed.return_value = FeedEntity(user_id=2)
    with pytest.raises(HTTPException):
        DeleteFeedUsecase().execute(payload={'user_id': 2}, feed_id=1)

    get_feed.return_value = FeedEntity(user_id=1)
    delete_feed.return_value = True
    # Case of success
    result = DeleteFeedUsecase().execute(payload={'user_id': 1}, feed_id=1)
    assert result is True


@patch('apps.repositories.FeedMySQLRepo.get_feed')
@patch('apps.repositories.FeedMySQLRepo.read_feed')
def test_read_feed(read_feed, get_feed):
    # Case of feed is None
    get_feed.return_value = None
    with pytest.raises(HTTPException):
        ReadFeedUsecase().execute(payload={'user_id': 1}, feed_id=1)

    # Case of permission denied
    get_feed.return_value = FeedEntity(id=1, user_id=2)
    with pytest.raises(HTTPException):
        ReadFeedUsecase().execute(payload={'user_id': 1}, feed_id=1)

    # Case of success
    get_feed.return_value = FeedEntity(id=1, user_id=1)
    result = ReadFeedUsecase().execute(payload={'user_id': 1}, feed_id=1)
    assert result is True
