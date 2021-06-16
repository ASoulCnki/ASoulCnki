import time

from dynamic_crawler import DynamicCrawler
from reply_crawler import ReplyCrawler

# 可爱的asoul成员们的uid捏
# asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094]
asoul_member_ids = [672346917]


def main():
    dynamic_crawler = DynamicCrawler()

    all_tuples = []
    for mid in asoul_member_ids:
        result = dynamic_crawler.crawl_all_dynamics(mid)
        all_tuples += result
    for tuple in all_tuples:
        r_crawler = ReplyCrawler(tuple[0], tuple[1])
        r_crawler.start_crawling_replies()
        time.sleep(0.1)


if __name__ == '__main__':
    main()
