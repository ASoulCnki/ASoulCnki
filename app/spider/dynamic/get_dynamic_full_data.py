import time
from app import models
from app.config import sqla
from app.spider.dynamic.dynamic_spider import crawl_dynamic_once, check_dynamic_already_exists


def create_request_and_save_data(member_id):
    session = sqla['session']

    time_start = time.time()
    print("start to crawl user dynamic with id {}".format(member_id))

    offset = 0
    finished = False
    while not finished:
        try:
            has_more, offset, tuples = crawl_dynamic_once(member_id, offset)

            for reply_tuple in tuples:
                dynamic = models.UserDynamic()
                dynamic.dynamic_id = reply_tuple[0]
                dynamic.type_id = reply_tuple[1]
                dynamic.oid = reply_tuple[2]
                dynamic.status = 0

                if check_dynamic_already_exists(session, dynamic):
                    finished = True
                    break
                else:
                    session.add(dynamic)
                    session.commit()
                    pass
        except Exception:
            return False
        if has_more == 0:
            break
    time_end = time.time()
    print("finished crawl dynamics for member {}, cost {}".format(member_id, time_end - time_start))
    return True


def task(member_ids, pool_number):
    session = sqla['session']
    state = session.query(models.KvStore).filter(models.KvStore.field_name == 'state').all()

    # see if the database is inited, if not, return directly
    if not len(state):
        return

    time_start = time.time()
    print("start to crawl user dynamic...")

    for member_id in member_ids:
        create_request_and_save_data(member_id)

    time_end = time.time()
    print('task to crawl all user dynamic cost', time_end - time_start, 's')
