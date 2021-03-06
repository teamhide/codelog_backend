from sqlalchemy import (Column, BigInteger, Unicode)

from app.entities import UserEntity
from core.databases import Base
from core.databases.mixin import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(Unicode(255))
    nickname = Column(Unicode(255))
    avatar_url = Column(Unicode(255))
    login_type = Column(Unicode(20), nullable=False)
    access_token = Column(Unicode(255), nullable=False)
    refresh_token = Column(Unicode(255), nullable=False)

    def to_entity(self):
        return UserEntity(
            id=self.id,
            email=self.email,
            nickname=self.nickname,
            avatar_url=self.avatar_url,
            login_type=self.login_type,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return f'' \
            f'User(id={self.id}, ' \
            f'email={self.email}, ' \
            f'nickname={self.nickname}, ' \
            f'avatar_url={self.avatar_url}, ' \
            f'login_type={self.login_type}, ' \
            f'access_token={self.access_token}, ' \
            f'refresh_token={self.refresh_token}, ' \
            f'created_at={self.created_at}, ' \
            f'updated_at={self.updated_at})'
