import abc
from typing import List, Union, Optional

from sqlalchemy import or_

from apps.entities import FeedEntity, TagEntity
from apps.models import Feed, Tag
from core.databases import session


class FeedRepo:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_feed(self, feed_id: int) -> Optional[FeedEntity]:
        pass

    @abc.abstractmethod
    def get_feed_list(
        self,
        user_id: int = None,
        prev: int = None,
    ) -> List[FeedEntity]:
        pass

    @abc.abstractmethod
    def create_feed(
        self,
        user_id: int,
        url: str,
        tags: List,
        image: str,
        title: str,
        description: str,
        is_private: bool,
    ) -> FeedEntity:
        pass

    @abc.abstractmethod
    def create_tag(self, name: Union[str, List], many: bool = False) -> None:
        pass

    @abc.abstractmethod
    def get_tag_list(self) -> List[TagEntity]:
        pass

    @abc.abstractmethod
    def search_feed(
        self,
        keyword: str,
        prev: int = None,
        user_id: int = None,
    ) -> List[FeedEntity]:
        pass

    @abc.abstractmethod
    def delete_feed(self, feed_id: int) -> None:
        pass


class FeedMySQLRepo(FeedRepo):
    def get_feed(self, feed_id: int):
        feed = session.query(Feed).filter(Feed.id == feed_id).first()

        if not feed:
            return None

        return feed.to_entity()

    def get_feed_list(
        self,
        user_id: int = None,
        prev: int = None,
    ) -> List[FeedEntity]:
        query = session.query(Feed)

        if user_id:
            query = query.filter(
                Feed.user_id == user_id,
            )
        else:
            query = query.filter(Feed.is_private == False)

        if prev:
            query = query.filter(Feed.id < prev)

        feeds = query.order_by(Feed.id.desc()).limit(10)

        return [
            feed.to_entity()
            for feed in feeds
        ]

    def create_feed(
        self,
        user_id: int,
        url: str,
        tags: List,
        image: str,
        title: str,
        description: str,
        is_private: bool,
    ) -> FeedEntity:
        feed = Feed(
            user_id=user_id,
            url=url,
            image=image,
            title=title,
            description=description,
            is_private=is_private,
        )

        for tag in tags:
            exist = session.query(Tag).filter(Tag.name == tag).first()
            if exist:
                feed.tags.append(exist)
            else:
                feed.tags.append(Tag(name=tag))

        session.add(feed)
        session.commit()

        return feed.to_entity()

    def create_tag(self, name: Union[str, List], many: bool = False) -> None:
        if many is True:
            tags = [
                row[0]
                for row in session.query(Tag)
                .filter(Tag.name.in_(name)).with_entities(Tag.name).all()
            ]
            for tag in list(set(name) - set(tags)):
                session.add(Tag(name=tag))
        else:
            pass

        session.commit()

    def get_tag_list(self) -> List[TagEntity]:
        tags = session.query(Tag).all()

        return [
            tag.to_entity()
            for tag in tags
        ]

    def search_feed(
        self,
        keyword: str,
        prev: int = None,
        user_id: int = None,
    ) -> List[FeedEntity]:
        query = session.query(Feed)

        if prev:
            query = query.filter(Feed.id < prev)

        if user_id:
            query = query.filter(Feed.user_id == user_id)
        else:
            query = query.filter(Feed.is_private == False)

        query = query.filter(
            or_(
                Feed.title.like(f'%{keyword}%'),
                Feed.description.like(f'%{keyword}%'),
            ),
        )

        feeds = query.order_by(Feed.id.desc()).limit(10)

        return [
            feed.to_entity()
            for feed in feeds
        ]

    def delete_feed(self, feed_id: int):
        feed = session.query(Feed).get(feed_id)

        session.delete(feed)
        session.commit()
