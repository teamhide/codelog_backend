from apps.entities import FeedEntity, TagEntity
from apps.models import Feed


def test_get_feed(create_feed_model, feed_repo):
    feed = feed_repo.get_feed(feed_id=1)

    assert isinstance(feed, FeedEntity)
    assert feed.id == create_feed_model.id
    assert feed.user_id == create_feed_model.user_id
    assert feed.image == create_feed_model.image
    assert feed.title == create_feed_model.title
    assert feed.description == create_feed_model.description
    assert feed.url == create_feed_model.url
    assert feed.is_private == create_feed_model.is_private
    assert feed.user.id == create_feed_model.user.id
    assert feed.user.email == create_feed_model.user.email
    assert feed.user.nickname == create_feed_model.user.nickname
    assert feed.user.avatar_url == create_feed_model.user.avatar_url
    assert feed.user.login_type == create_feed_model.user.login_type
    assert feed.user.access_token == create_feed_model.user.access_token
    assert feed.user.refresh_token == create_feed_model.user.refresh_token


def test_get_feed_list(create_feed_model_list, feed_repo):
    feeds = feed_repo.get_feed_list(user_id=1)
    db_feeds = list(reversed(create_feed_model_list))

    assert len(feeds) == len(create_feed_model_list)
    for a, b in zip(feeds, db_feeds):
        assert a.id == b.id
        assert a.user_id == b.user_id
        assert a.image == b.image
        assert a.title == b.title
        assert a.description == b.description
        assert a.url == b.url
        assert a.is_private == b.is_private
        assert a.user.id == b.user.id
        assert a.user.email == b.user.email
        assert a.user.nickname == b.user.nickname
        assert a.user.avatar_url == b.user.avatar_url
        assert a.user.login_type == b.user.login_type
        assert a.user.access_token == b.user.access_token
        assert a.user.refresh_token == b.user.refresh_token


def test_create_feed(session, feed_repo, create_user_model):
    feed = feed_repo.create_feed(
        user_id=1,
        url='http://hides.kr',
        tags=['python', 'msa'],
        image='test image',
        title='test title',
        description='test description',
        is_private=False,
    )

    assert feed.id == 1
    assert feed.url == 'http://hides.kr'
    assert feed.tags == ['python', 'msa']
    assert feed.image == 'test image'
    assert feed.title == 'test title'
    assert feed.description == 'test description'
    assert feed.is_private is False


def test_create_tag(session, feed_repo):
    tag = feed_repo.create_tag(name='python', many=False)
    assert tag is None

    tags = feed_repo.create_tag(name=['python', 'golang'], many=True)
    assert tags is None


def test_get_tag_list(session, feed_repo, create_tag_model):
    tags = feed_repo.get_tag_list()

    assert type(tags) == list
    assert isinstance(tags[0], TagEntity)
    assert tags[0].id == 1
    assert tags[0].name == 'python'


def test_search_feed(session, feed_repo, create_feed_model):
    feed = feed_repo.search_feed(keyword='none')
    assert type(feed) == list

    feed = feed_repo.search_feed(keyword='test')
    assert type(feed) == list
    assert feed[0].id == create_feed_model.id
    assert feed[0].id == create_feed_model.id
    assert feed[0].user_id == create_feed_model.user_id
    assert feed[0].image == create_feed_model.image
    assert feed[0].title == create_feed_model.title
    assert feed[0].description == create_feed_model.description
    assert feed[0].url == create_feed_model.url
    assert feed[0].is_private == create_feed_model.is_private
    assert feed[0].user.id == create_feed_model.user.id
    assert feed[0].user.email == create_feed_model.user.email
    assert feed[0].user.nickname == create_feed_model.user.nickname
    assert feed[0].user.avatar_url == create_feed_model.user.avatar_url
    assert feed[0].user.login_type == create_feed_model.user.login_type
    assert feed[0].user.access_token == create_feed_model.user.access_token
    assert feed[0].user.refresh_token == create_feed_model.user.refresh_token


def test_delete_feed(session, feed_repo, create_feed_model):
    feed = session.query(Feed).filter(Feed.id == create_feed_model.id).first()
    assert feed is not None

    feed_repo.delete_feed(feed_id=create_feed_model.id)
    feed = session.query(Feed).filter(Feed.id == create_feed_model.id).first()
    assert feed is None
