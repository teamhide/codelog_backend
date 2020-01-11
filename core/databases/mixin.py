from datetime import datetime

from sqlalchemy import Column, DateTime


class TimestampMixin:
    created_at = Column(
        DateTime,
        default=datetime.utcnow().replace(microsecond=0),
        nullable=False, )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow().replace(microsecond=0),
        onupdate=datetime.utcnow().replace(microsecond=0),
        nullable=False,
    )
