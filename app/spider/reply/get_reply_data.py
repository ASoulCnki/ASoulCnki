import time

import app.models as models
from app.config import sqla
from app.spider.reply.reply_spider import crawl_reply_once, check_reply_already_exists


def create_request_and_save_data(reply_param_tuple):
    session = sqla['session']

    print("start to crawl reply with param {}".format(reply_param_tuple))

    type_id = reply_param_tuple[0]
    oid = reply_param_tuple[1]
    status = reply_param_tuple[2]
    dynamic_id = reply_param_tuple[3]

    page_size = 49
    next_offset = 0
    finished = False
    while not finished:
        try:
            is_end, next_offset, result = crawl_reply_once(oid, type_id, dynamic_id, page_size, next_offset)
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
            session.rollback()
            raise e

    # modify status
    if status == 0:
        try:
            dynamic = session.query(models.UserDynamic).filter(models.UserDynamic.oid == oid).one()
            dynamic.status = 1
            session.add(dynamic)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


def task(tuples, pool_number):
    time_start = time.time()

    for reply_param_tuple in tuples:
        create_request_and_save_data(reply_param_tuple)

    time_end = time.time()
    print('crawl reply cost', time_end - time_start, 's')
