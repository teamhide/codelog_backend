from flask import jsonify

from apps.schemas import OAuthLoginResponseSchema, RefreshTokenSchema
from apps.usecases import Token
from core.presenters import Presenter


class OAuthLoginPresenter(Presenter):
    @classmethod
    def transform(cls, response: Token) -> jsonify:
        return jsonify(OAuthLoginResponseSchema().dump(response))


class RefreshTokenPresenter(Presenter):
    @classmethod
    def transform(cls, response: Token) -> jsonify:
        return jsonify(RefreshTokenSchema().dump(response))


class VerifyTokenPresenter(Presenter):
    @classmethod
    def transform(cls, response) -> jsonify:
        return jsonify({'status': response})
