from flask import jsonify, request

from app.lib.duplication_check.check import get_database
from app.lib.duplication_check.reply_database import ReplyDatabase
from app.lib.red_print import RedPrint
from app.config import sqla
import app.models as models
from app.lib.error_code import ServerError

api = RedPrint('reply_source')

reply_db: ReplyDatabase = get_database()


@api.route('/reset', methods=['POST'], strict_slashes=False)
def reset_reply_database():
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
def reset_reply_source():
    start_rpid = request.json.get("start_rpid")
    session = sqla["session"]
    try:
        result = session.query(models.Reply).filter(models.Reply.rpid > start_rpid).all()
        if len(result) != 0:
            with reply_db.lock.gen_wlock():
                for r in result:
                    reply_db.add_reply_data(r)
            reply_db.dump_to_image("database.dat")
        return_dict = {
            "code": 0,
            "message": "",
            "data": {
                "start_time": reply_db.min_time,
                "end_time": reply_db.max_time,
            }}
        return jsonify(return_dict)
    except Exception:
        raise ServerError()


@api.route('/checkpoint', methods=['POST'], strict_slashes=False)
def do_checkpoint_for_reply_database():
    reply_db.dump_to_image("database.dat")
    return_dict = {
        "code": 0,
        "message": "",
        "data": {
            "start_time": reply_db.min_time,
            "end_time": reply_db.max_time,
        }}
    return jsonify(return_dict)
