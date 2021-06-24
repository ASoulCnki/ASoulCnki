import app.models as models
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from app import utils
from app.utils import Throttle

throttle = Throttle(0.5)


def crawl_reply_once(oid, type_id, page_size, next_offset):
    url = "https://api.bilibili.com/x/v2/reply/main?oid={}&type={}&next={}&mode={}&ps={}" \
        .format(oid, type_id, next_offset, 2, page_size)
    # do throttle control before requesting url
    throttle.wait_url("https://api.bilibili.com/x/v2/reply/main")
    r = utils.url_get(url=url, mode="json")

    if ("code" not in r) or r["code"] != 0:
        raise ValueError("Error response code: {}".format(r["code"]))

    data = r["data"]

    # there is no more reply, finish crawling
    if "replies" not in data or (data["replies"] is None):
        return True, 0, []

    result = []

    replies = data["replies"]
    for reply in replies:
        reply_entry = models.Reply()
        reply_entry.rpid = reply["rpid"]
        reply_entry.type_id = reply["type"]
        reply_entry.mid = reply["mid"]
        reply_entry.oid = reply["oid"]
        reply_entry.ctime = reply["ctime"]
        reply_entry.m_name = reply["member"]["uname"]
        reply_entry.content = reply["content"]["message"]
        reply_entry.like_num = reply["like"]
        reply_entry.json_text = ''
        result.append(reply_entry)

    # read cursor data to see weather we need to return
    cursor = data["cursor"]
    new_next_offset = cursor["next"]
    is_end = cursor["is_end"]

    if next_offset == 0:
        print("oid: {} type id: {} all count: {}".format(oid, type_id, cursor["all_count"]))

    return is_end, new_next_offset, result


def check_reply_already_exists(session, reply: models.Reply):
    reply_class = models.Reply
    try:
        session.query(reply_class).filter(reply_class.rpid == reply.rpid).one()
        return True
    except NoResultFound:
        return False
    except MultipleResultsFound:
        return True
