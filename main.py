from app import create_app
from core.settings import get_config


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        debug=False if get_config().env == 'production' else True,
        port=8000,
    )
