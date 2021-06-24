from flask_cors import CORS
from .app import Flask

cors = CORS(supports_credentials=True)


def register_blueprints(flask_app):
    from app.api.v1 import create_blueprint_v1
    from app.api.frontend import create_blueprint_view

    flask_app.register_blueprint(create_blueprint_v1(), url_prefix='/v1/api')
    flask_app.register_blueprint(create_blueprint_view(), url_prefix='/')


def register_plugin(flask_app):
    # 注册cors
    cors.init_app(flask_app)
    # register more app like database


def create_app():
    flask_app = Flask(__name__, static_url_path='', static_folder="frontend")

    register_blueprints(flask_app)
    register_plugin(flask_app)

    return flask_app
