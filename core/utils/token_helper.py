from datetime import datetime, timedelta

import jwt
from core.exceptions import abort
from core.settings import get_config


class TokenHelper:
    @classmethod
    def decode_expired_token(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                get_config().jwt_secret_key,
                algorithms=[get_config().jwt_algorithm],
                options={'verify_exp': False}
            )
        except jwt.exceptions.DecodeError:
            abort(401, error='invalid token')

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                get_config().jwt_secret_key,
                algorithms=[get_config().jwt_algorithm],
            )
        except jwt.exceptions.DecodeError:
            abort(401, error='invalid token')
        except jwt.exceptions.ExpiredSignatureError:
            abort(401, error='token expired')

    @classmethod
    def encode(cls, payload: dict, expire_period: int = 3600):
        return jwt.encode(
            payload={
                **payload,
                'exp': datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=get_config().jwt_secret_key,
            algorithm=get_config().jwt_algorithm,
        )
