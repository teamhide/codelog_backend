from functools import wraps

from flask import request

from core.utils import TokenHelper


def is_jwt_authenticated():
    def _is_jwt_authenticated(f):
        @wraps(f)
        def __is_jwt_authenticated(*args, **kwargs):
            payload = TokenHelper.decode(token=request.headers.get('Authorization').split()[1])
            return f(*args, **kwargs, payload=payload)
        return __is_jwt_authenticated
    return _is_jwt_authenticated
