from flask import Blueprint, request
from marshmallow import ValidationError

from apps.presenters import (
    OAuthLoginPresenter,
    RefreshTokenPresenter,
    VerifyTokenPresenter,
)
from apps.schemas import (
    OAuthLoginRequestSchema,
    RefreshTokenSchema,
    VerityTokenRequestSchema,
)
from apps.usecases import (
    GithubLoginUsecase,
    GoogleLoginUsecase,
    KakaoLoginUsecase,
    RefreshTokenUsecase,
    VerifyTokenUsecase,
)
from core.exceptions import abort

oauth_bp = Blueprint('oauth', __name__, url_prefix='/oauth')


@oauth_bp.route('/github/login', methods=['GET'])
def github_login():
    try:
        validator = OAuthLoginRequestSchema().load(data=request.args)
    except ValidationError:
        abort(400, error='validation error')

    token = GithubLoginUsecase().execute(**validator)
    return OAuthLoginPresenter.transform(response=token)


@oauth_bp.route('/google/login', methods=['GET'])
def google_login():
    token = GoogleLoginUsecase().execute(code=request.args.get('code'))
    return {'status': True}


@oauth_bp.route('/kakao/login', methods=['GET'])
def kakao_login():
    token = KakaoLoginUsecase().execute(code=request.args.get('code'))
    return 'Hello'


@oauth_bp.route('/refresh_token', methods=['POST'])
def refresh_token():
    try:
        validator = RefreshTokenSchema().load(data=request.form)
    except ValidationError:
        abort(400, error='validation error')

    token = RefreshTokenUsecase().execute(**validator)
    return RefreshTokenPresenter.transform(response=token)


@oauth_bp.route('/verify_token', methods=['POST'])
def verify_token():
    try:
        validator = VerityTokenRequestSchema().load(data=request.form)
    except ValidationError:
        abort(400, error='validation error')

    if VerifyTokenUsecase().execute(**validator):
        return VerifyTokenPresenter.transform(response=True)
