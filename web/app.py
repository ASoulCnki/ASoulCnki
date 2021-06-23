from flask import Flask, Blueprint, jsonify, request, current_app
from flask_cors import CORS

from duplication_check.check import get_database
from duplication_check.check import check_v2 as check

database = get_database()

api_bp = Blueprint("api", __name__, url_prefix='/v1/api')
view_bp = Blueprint("view", __name__, url_prefix='/')


@api_bp.route('/check', methods=['get', 'post'])
def route_check():
    src_text = request.json.get("text")
    check_data = check(database, src_text, 5)
    (rate, text) = check_data.pop()
    related = []
    while(check_data):
        passage = check_data.pop()
        related.append(
            {"rate": passage[0], "text": passage[1], "author": "暂不公开"})
    data = {"rate":rate, "start_time":1624237336, "end_time":1624238336,"related":related}
    return_dict = {"code": 0, "message": "","data":data}
    return jsonify(return_dict)


@view_bp.route('/', methods=['GET'])
@view_bp.route('/index', methods=['GET'])
def route_index():
    return current_app.send_static_file("index.html")

@view_bp.route('/m_index', methods=['GET'])
def route_m_index():
    return current_app.send_static_file("m_index.html")

@view_bp.route('/result', methods=['GET'])
def route_result():
    return current_app.send_static_file("result.html")

@view_bp.route('/protocal', methods=['GET'])
def route_protocal():
    return current_app.send_static_file("protocal.html")


def create_app():
    app = Flask(__name__, static_url_path='', static_folder="frontend")
    CORS(app, supports_credentials=True)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(api_bp)
    app.register_blueprint(view_bp)


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
