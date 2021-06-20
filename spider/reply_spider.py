import json

from spider.util import utils
from spider.util.throttle import Throttle


class ReplySpider:

    def __init__(self, type_id, oid, throttle: Throttle = None):
        self.type_id = type_id
        self.oid = oid
        self.next = 0
        self.page_size = 49
        self.finished = False
        if throttle is not None:
            self.throttle = throttle
        else:
            self.throttle = Throttle(0.05)

    def start_crawling_replies(self):
        throttle = Throttle(0.05)
        result = []
        while not self.finished:
            url = "https://api.bilibili.com/x/v2/reply/main?oid={}&type={}&next={}&mode={}&ps={}" \
                .format(self.oid, self.type_id, self.next, 2, self.page_size)
            # do throttle control before requesting url
            throttle.wait_url("https://api.bilibili.com/x/v2/reply/main")
            r = utils.url_get(url=url, mode="json")

            if ("code" not in r) or r["code"] != 0:
                raise ValueError("Error response code: {}".format(r["code"]))

            data = r["data"]

            # there is no more reply, finish crawling
            if "replies" not in data or (data["replies"] is None):
                self.finished = True
                break

            replies = data["replies"]
            for reply in replies:
                result.append({
                    "rpid": reply["rpid"],
                    "type": reply["type"],
                    "mid": reply["mid"],
                    "oid": reply["oid"],
                    "ctime": reply["ctime"],
                    "m_name": reply["member"]["uname"],
                    "content": reply["content"]["message"],
                    "like_num": reply["like"],
                    "json_text": json.dumps(data)
                })

            # read cursor data to see weather we need to return
            cursor = data["cursor"]
            self.next = cursor["next"]
            if cursor["is_end"]:
                self.finished = True
                break

            print("replies count: {}".format(len(replies)))
        return result
