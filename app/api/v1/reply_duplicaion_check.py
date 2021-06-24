import time

from flask import request, jsonify
from app.lib.duplication_check.check import get_database
from app.lib.duplication_check.check import check
from app.lib.red_print import RedPrint

reply_db = get_database()

api = RedPrint('check')


@api.route('/', methods=['POST'], strict_slashes=False)
def check_duplication():
    start_time = time.time()
    src_text = request.json.get("text")
    check_result = check(reply_db, src_text, 5)
    end_time = time.time()
    return_dict = {
        "code": 0,
        "message": "",
        "data": {
            "rate": check_result[2],
            "start_time": start_time,
            "end_time": end_time,
            "related": check_result[0]
        }}
    return jsonify(return_dict)
