from app.utils.throttle import Throttle
from app.utils.request_util import *

throttle = Throttle(0.05)

bilibili_dynamic_url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"


def crawl_dynamic_once(mid, offset):
    url = bilibili_dynamic_url + "?host_uid={}&offset_dynamic_id={}&platform=web". \
        format(mid, offset)

    throttle.wait_url(bilibili_dynamic_url)

    r = url_get(url=url, mode="json")

    if ("code" not in r) or r["code"] != 0:
        raise ValueError("Error response code: {}".format(r["code"]))

    # read vars from response
    data = r["data"]
    return parse_dynamic_data(data)


def parse_dynamic_data(data):
    next_offset = data["next_offset"]
    has_more = data["has_more"]
    tuples = []
    if "cards" not in data:
        return 0, 0, tuples

    cards = data["cards"]
    for card in cards:

        dynamic_type = card["desc"]["type"]
        dynamic_id = card["desc"]["dynamic_id"]
        rid = card["desc"]["rid"]

        # we need to map dynamic type to reply type, and choose right reply oid,
        # see https://github.com/SocialSisterYi/bilibili-API-collect/tree/master/comment

        oid = 0
        r_type = 0
        if dynamic_type == 1 or dynamic_type == 4:
            r_type = 17
            oid = dynamic_id
        elif dynamic_type == 2:
            r_type = 11
            oid = rid
        elif dynamic_type == 8:
            r_type = 1
            oid = rid
        elif dynamic_type == 64:
            r_type = 12
            oid = rid
        # TODO: add more reply type and mapping
        else:
            print("type: {} desc: {} card: {} ".format(dynamic_type, card["desc"], card["card"]))
            # TODO: raise an exception
        tuples.append((dynamic_id, r_type, oid))

    return has_more, next_offset, tuples
