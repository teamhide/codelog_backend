from flask import Flask
from flask_cors import CORS
from pythondi import Provider, configure

from app.repositories import FeedRepo, FeedMySQLRepo, UserRepo, UserMySQLRepo
from app.views import feed_bp, user_bp, oauth_bp, home_bp
from core.databases import session
from core.settings import get_config


def init_listeners(app: Flask):
    @app.teardown_appcontext
    def shutdown_session(response):
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

    if get_config().env == 'production':
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=get_config().sentry_dsn,
            integrations=[FlaskIntegration(), SqlalchemyIntegration()]
        )

    @app.route('/debug-sentry')
    def trigger_error():
        division_by_zero = 1 / 0


def init_di(app: Flask):
    provider = Provider()
    provider.bind(FeedRepo, FeedMySQLRepo)
    provider.bind(UserRepo, UserMySQLRepo)
    configure(provider=provider)


def create_app():
    app = Flask(__name__)
    init_blueprint(app=app)
    init_listeners(app=app)
    init_extensions(app=app)
    init_di(app=app)
    return app
