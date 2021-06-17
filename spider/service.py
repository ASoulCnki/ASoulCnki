import time

from dynamic_spider import DynamicSpider
from reply_spider import ReplySpider
from spider.util.throttle import Throttle


class ASoulCnkiSpiderService:
    def __init__(self, member_ids):
        # member ids to crawl
        self.member_ids = member_ids

    def start(self):
        throttle = Throttle(0.05)
        dynamic_crawler = DynamicSpider(throttle)

        all_tuples = []
        for mid in self.member_ids:
            result = dynamic_crawler.crawl_all_dynamics(mid)
            all_tuples += result
        for reply_spider_param_tuple in all_tuples:
            type_id = reply_spider_param_tuple[0]
            oid = reply_spider_param_tuple[1]
            r_crawler = ReplySpider(type_id, oid, throttle)
            r_crawler.start_crawling_replies()
            time.sleep(0.1)


if __name__ == '__main__':
    # 可爱的asoul成员们的uid捏
    asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094]
    # 测试就只用晚晚的id😈
    # asoul_member_ids = [672346917]
    asoul_cnki_spider_service = ASoulCnkiSpiderService(asoul_member_ids)
    asoul_cnki_spider_service.start()
