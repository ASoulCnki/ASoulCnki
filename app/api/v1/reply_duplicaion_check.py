from flask import request, jsonify

from app.lib.duplication_check.reply_database import reply_db_singleton as reply_db
from app.lib.duplication_check.check import check
from app.lib.red_print import RedPrint
from app.lib.error_code import Forbidden

api = RedPrint('check')


@api.route('/', methods=['POST'], strict_slashes=False)
def check_duplication():
    src_text = request.json.get("text")
    if len(src_text) > 1000:
        raise Forbidden()
    check_result = check(reply_db, src_text, 5)
    return_dict = {
        "code": 0,
        "message": "",
        "data": {
            "rate": check_result[2],
            "start_time": reply_db.min_time,
            "end_time": reply_db.max_time,
            "related": check_result[0]
        }}
    return jsonify(return_dict)
