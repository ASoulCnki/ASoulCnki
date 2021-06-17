from spider import utils


class DynamicSpider:

    # def __init__(self, member_ids, meta_storage):
    #     self.member_ids = member_ids
    #     self.meta_storage = meta_storage

    def crawl_all_dynamics(self, member_id):
        result = []
        offset = 0
        while True:
            has_more, offset, tuples = self._crawl_dynamic_once(member_id, offset)
            result += tuples
            if has_more == 0:
                break
        return result

    @staticmethod
    def _crawl_dynamic_once(mid, offset):
        print("mid: {} offset: {}".format(mid, offset))
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history" \
              "?host_uid={}&offset_dynamic_id={}&platform=web". \
            format(mid, offset)
        r = utils.url_get(url=url, mode="json")

        if ("code" not in r) or r["code"] != 0:
            raise ValueError("Error response code: {}".format(r["code"]))

        # read vars from response
        data = r["data"]
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
            tuples.append((r_type, oid))

        return has_more, next_offset, tuples
