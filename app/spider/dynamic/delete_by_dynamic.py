import time

from app import models
from app.config import sqla
from app.spider.dynamic.dynamic_spider import crawl_dynamic_once


# crawl all dynamic for one user and store them to database
def create_requests_and_save_data(member_id):
    session = sqla['session']

    time_start = time.time()
    print("start to crawl user dynamic with id {}".format(member_id))

    result = []
    offset = 0
    while True:
        try:
            has_more, offset, tuples = crawl_dynamic_once(member_id, offset)
            for reply_tuple in tuples:
                dynamic = models.UserDynamic()
                dynamic.dynamic_id = reply_tuple[0]
                dynamic.type_id = reply_tuple[1]
                dynamic.oid = reply_tuple[2]
                session.query(models.UserDynamic).filter(models.UserDynamic.dynamic_id == dynamic.dynamic_id).delete()
                session.query(models.Reply).filter(models.Reply.dynamic_id == dynamic.dynamic_id).delete()
                session.commit()
        except Exception:
            return False
        result += tuples
        if has_more == 0:
            break

    time_end = time.time()
    print("finished crawl dynamics for member {}, cost {}".format(member_id, time_end - time_start))
    return True


if __name__ == '__main__':
    create_requests_and_save_data(703007996)
