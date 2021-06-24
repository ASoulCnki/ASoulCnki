from flask import current_app

from app.lib.red_print import RedPrint

api = RedPrint('/')


@api.route('/', methods=['GET'], strict_slashes=False)
@api.route('/index', methods=['GET'])
def route_index():
    return current_app.send_static_file("index.html")


@api.route('/m_index', methods=['GET'])
def route_m_index():
    return current_app.send_static_file("m_index.html")


@api.route('/result', methods=['GET'])
def route_result():
    return current_app.send_static_file("result.html")


@api.route('/protocol', methods=['GET'])
def route_protocal():
    return current_app.send_static_file("protocol.html")
