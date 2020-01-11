from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Unicode,
    ForeignKey,
    Table,
    Boolean
)
from sqlalchemy.orm import relationship

from apps.entities import FeedEntity, TagEntity
from core.databases import Base
from core.databases.mixin import TimestampMixin

feed_tag = Table(
    'feed_tag',
    Base.metadata,
    Column('feed_id', ForeignKey('feeds.id')),
    Column('tag_id', ForeignKey('tags.id')),
)


class Feed(Base, TimestampMixin):
    __tablename__ = 'feeds'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    image = Column(Unicode(255), nullable=True)
    title = Column(Unicode(255), nullable=True)
    description = Column(Unicode(255), nullable=True)
    url = Column(Unicode(255), nullable=False)
    user = relationship('User', uselist=False)
    tags = relationship('Tag', secondary=feed_tag, back_populates='feeds')
    is_private = Column(Boolean, default=True)

    def to_entity(self):
        return FeedEntity(
            id=self.id,
            user_id=self.user_id,
            image=self.image,
            title=self.title,
            description=self.description,
            url=self.url,
            user=self.user.to_entity(),
            tags=[
                tag.name
                for tag in self.tags
            ],
            is_private=self.is_private,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(30), nullable=False, unique=True)
    feeds = relationship('Feed', secondary=feed_tag, back_populates='tags')

    def to_entity(self):
        return TagEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
