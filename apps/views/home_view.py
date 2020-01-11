from flask import Blueprint


home_bp = Blueprint('home', __name__, url_prefix='/')


@home_bp.route('/', methods=['GET'])
def home():
    return {'status': True}
