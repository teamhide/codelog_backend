from flask import Blueprint

user_bp = Blueprint('users', __name__, url_prefix='/api/users')


@user_bp.route('/', methods=['GET'])
def home():
    return 'Hello'
