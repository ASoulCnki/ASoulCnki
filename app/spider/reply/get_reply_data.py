import time

import app.models as models
from app.config import sqla
from app.spider.reply.reply_spider import crawl_reply_once, check_reply_already_exists
from pymysql.err import IntegrityError


def create_request_and_save_data(type_id, oid, status, dynamic_id):
    session = sqla['session']

    print("start to crawl reply with dynamic id {}, status {}".format(dynamic_id, status))

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
        except IntegrityError:  # another spider is executing the same task
            continue
        except Exception as e:
            session.rollback()
            raise e

    # modify status
    if status == 0:
        try:
            dynamic = session.query(models.UserDynamic).filter(models.UserDynamic.dynamic_id == dynamic_id).one()
            dynamic.status = 1
            session.add(dynamic)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


def task(type_id, oid, status, dynamic_id):
    time_start = time.time()
    create_request_and_save_data(type_id, oid, status, dynamic_id)

    time_end = time.time()
    print('crawl reply cost', time_end - time_start, 's')
