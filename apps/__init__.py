import sentry_sdk
from flask import Flask
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from apps.views import feed_bp, user_bp, oauth_bp, home_bp
from core.databases import session
from core.settings import get_config


def init_listeners(app: Flask):
    @app.after_request
    def after_request(response):
        session.remove()
        return response


def init_middlewares(app: Flask):
    pass


def init_blueprint(app: Flask):
    app.register_blueprint(feed_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(home_bp)


def init_extensions(app: Flask):
    CORS(app)
    sentry_sdk.init(
        dsn=get_config().sentry_dsn,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()]
    )

    @app.route('/debug-sentry')
    def trigger_error():
        division_by_zero = 1 / 0


def create_app():
    app = Flask(__name__)
    init_blueprint(app=app)
    init_listeners(app=app)
    init_extensions(app=app)
    return app
