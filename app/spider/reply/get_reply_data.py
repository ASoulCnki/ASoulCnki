import time

from gevent.pool import Pool

from app.config import sqla
from app.spider.reply.reply_spider import crawl_reply_once, check_reply_already_exists
import app.models as models


def create_request_and_save_data(reply_param_tuple):
    session = sqla['session']
    type_id = reply_param_tuple[0]
    oid = reply_param_tuple[1]
    status = reply_param_tuple[2]

    page_size = 49
    next_offset = 0
    finished = False
    while not finished:
        try:
            is_end, next_offset, result = crawl_reply_once(oid, type_id, page_size, next_offset)
            for reply in result:
                already_exists = check_reply_already_exists(session, reply)
                if status == 0:
                    if not already_exists:
                        session.add(reply)
                        session.commit()
                else:
                    if already_exists:
                        finished = True
                        break
                    else:
                        session.add(reply)
                        session.commit()
            if is_end:
                break
        except Exception as e:
            print(e)
            session.rollback()
            return

    # modify status
    if status == 0:
        try:
            dynamic = session.query(models.UserDynamic).filter(models.UserDynamic.oid == oid).one()
            dynamic.status = 1
            session.add(dynamic)
            session.commit()
        except Exception as e:
            session.rollback()


def task(tuples, pool_number):
    time_start = time.time()

    pool = Pool(pool_number)
    for reply_param_tuple in tuples:
        pool.spawn(
            create_request_and_save_data,
            reply_param_tuple=reply_param_tuple,
        )
    pool.join()

    time_end = time.time()
    print('crawl reply cost', time_end - time_start, 's')
