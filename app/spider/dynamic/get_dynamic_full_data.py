import time
from gevent.pool import Pool
from app import models
from app.config import sqla
from app.spider.dynamic.dynamic_spider import crawl_dynamic_once
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


def create_request_and_save_data(member_id):
    session = sqla['session']

    time_start = time.time()
    print("start to crawl user dynamic with id {}".format(member_id))

    offset = 0
    finished = False
    dynamic_class = models.UserDynamic
    while not finished:
        try:
            has_more, offset, tuples = crawl_dynamic_once(member_id, offset)

            for reply_tuple in tuples:
                dynamic = models.UserDynamic()
                dynamic.dynamic_id = reply_tuple[0]
                dynamic.type_id = reply_tuple[1]
                dynamic.oid = reply_tuple[2]
                dynamic.status = 0

                try:
                    session.query(dynamic_class).filter(dynamic_class.dynamic_id == dynamic.dynamic_id).one()
                    finished = True
                    break
                except NoResultFound:
                    print("add dynamic with id {} to database".format(dynamic.dynamic_id))
                    session.add(dynamic)
                    session.commit()
                    pass
                except MultipleResultsFound:
                    finished = True
                    break
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

    pool = Pool(pool_number)
    g_result = []
    for member_id in member_ids:
        result = pool.spawn(
            create_request_and_save_data,
            member_id=member_id,
        )
        g_result.append(result)
    pool.join()

    time_end = time.time()
    print('task to crawl all user dynamic cost', time_end - time_start, 's')
