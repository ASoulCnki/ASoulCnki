from flask import jsonify, request

from app.lib.duplication_check.reply_database import reply_db_singleton as reply_db
from app.lib.error_code import ServerError
from app.lib.red_print import RedPrint
from app.lib.duplication_check.pull_data import pull_data_from_database
from app.config.secure import CONTROL_SECURE_KEY

api = RedPrint('reply_source')


@api.route('/reset', methods=['POST'], strict_slashes=False)
def reset_reply_database():
    secure_key = request.json.get("secure_key")
    if secure_key != CONTROL_SECURE_KEY:
        raise ServerError()
    reply_db.reset()
    reply_db.dump_to_image("database.dat")
    return_dict = {
        "code": 0,
        "message": "",
        "data": {
            "start_time": reply_db.min_time,
            "end_time": reply_db.max_time,
        }}
    return jsonify(return_dict)


@api.route('/pull', methods=['POST'], strict_slashes=False)
def pull_data_from_data_source():
    secure_key = request.json.get("secure_key")
    if secure_key != CONTROL_SECURE_KEY:
        raise ServerError()
    start_time = request.json.get("start_time")
    try:
        pull_data_from_database(reply_db, start_time)
        return_dict = {
            "code": 0,
            "message": "",
            "data": {
                "start_time": reply_db.min_time,
                "end_time": reply_db.max_time,
            }}
        return jsonify(return_dict)
    except Exception as e:
        print(e)
        raise ServerError()


@api.route('/checkpoint', methods=['POST'], strict_slashes=False)
def do_checkpoint_for_reply_database():
    secure_key = request.json.get("secure_key")
    if secure_key != CONTROL_SECURE_KEY:
        raise ServerError()
    reply_db.dump_to_image("database.dat")
    return_dict = {
        "code": 0,
        "message": "",
        "data": {
            "start_time": reply_db.min_time,
            "end_time": reply_db.max_time,
        }}
    return jsonify(return_dict)
