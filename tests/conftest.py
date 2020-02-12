import pytest
from pythondi import Provider, configure_after_clear

from app.models import Feed, User, Tag
from app.repositories import FeedRepo, FeedMySQLRepo, UserRepo, UserMySQLRepo
from core.databases import Base, engine, session as db_session


@pytest.fixture
def init_di():
    provider = Provider()
    provider.bind(FeedRepo, FeedMySQLRepo)
    provider.bind(UserRepo, UserMySQLRepo)
    configure_after_clear(provider=provider)


@pytest.yield_fixture
def session():
    Base.metadata.create_all(engine)
    yield db_session
    db_session.remove()
    Base.metadata.drop_all(engine)


@pytest.fixture
def feed_repo():
    return FeedMySQLRepo()


@pytest.fixture
def user_repo():
    return UserMySQLRepo()


@pytest.fixture
def create_user_model(session):
    user = User(
        id=1,
        email='padocon@naver.com',
        nickname='hide',
        avatar_url='test avatar',
        login_type='github',
        access_token='test access_token',
        refresh_token='test refresh_token',
    )
    session.add(user)
    session.commit()


@pytest.fixture
def create_feed_model(session, create_user_model):
    feed = Feed(
        user_id=1,
        image='test image',
        title='test title',
        description='test description',
        url='http://hides.kr',
        is_private=False,
    )
    session.add(feed)
    session.commit()
    return feed


@pytest.fixture
def create_feed_model_list(session, create_user_model):
    feed_1 = Feed(
        user_id=1,
        image='test image 1',
        title='test title 1',
        description='test description 1',
        url='http://hides.kr 1',
        is_private=True,
    )
    feed_2 = Feed(
        user_id=1,
        image='test image 2',
        title='test title 2',
        description='test description 2',
        url='http://hides.kr 2',
        is_private=True,
    )
    session.add_all([feed_1, feed_2])
    session.commit()
    return [feed_1, feed_2]


@pytest.fixture
def create_tag_model(session):
    tag = Tag(
        name='python'
    )
    session.add(tag)
    session.commit()
    return tag
