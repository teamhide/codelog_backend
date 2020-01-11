from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int = None
    email: str = None
    nickname: str = None
    avatar_url: str = None
    login_type: str = None
    access_token: str = None
    refresh_token: str = None
    created_at: datetime = None
    updated_at: datetime = None
