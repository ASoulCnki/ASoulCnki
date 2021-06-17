import time

from dynamic_spider import DynamicSpider
from reply_spider import ReplySpider
from throttle import Throttle

# 可爱的asoul成员们的uid捏
# asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094]
asoul_member_ids = [672346917]


def main():
    throttle = Throttle(0.05)
    dynamic_crawler = DynamicSpider(throttle)

    all_tuples = []
    for mid in asoul_member_ids:
        result = dynamic_crawler.crawl_all_dynamics(mid)
        all_tuples += result
    for tuple in all_tuples:
        r_crawler = ReplySpider(tuple[0], tuple[1], throttle)
        r_crawler.start_crawling_replies()
        time.sleep(0.1)


if __name__ == '__main__':
    main()
