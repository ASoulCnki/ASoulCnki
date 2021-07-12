import time

import app.models as models
from app.config import sqla
from app.config.const import *
from app.spider.dynamic.dynamic_spider import crawl_dynamic_once, check_dynamic_already_exists


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
        except Exception:
            return False
        result += tuples
        if has_more == 0:
            break

    for reply_tuple in result:
        dynamic = models.UserDynamic()
        dynamic.dynamic_id = reply_tuple[0]
        dynamic.type_id = reply_tuple[1]
        dynamic.oid = reply_tuple[2]
        dynamic.ctime = reply_tuple[3]
        dynamic.status = 0
        if check_dynamic_already_exists(session, dynamic):
            continue
        session.add(dynamic)
        session.commit()

    time_end = time.time()
    print("finished crawl dynamics for member {}, cost {}".format(member_id, time_end - time_start))
    return True


def task(member_ids, pool_number):
    session = sqla['session']
    state = session.query(models.KvStore).filter(models.KvStore.field_name == 'state').all()

    # duplication_check if the database is inited, if not, do initialization
    if not len(state):

        session.execute("truncate table user_dynamic")

        time_start = time.time()
        print("start to crawl user dynamic...")

        g_result = []
        for member_id in member_ids:
            result = create_requests_and_save_data(member_id)
            g_result.append(result)

        # duplication_check whether all tasks finished correctly
        all_finished = True
        for r in g_result:
            all_finished = r & all_finished

        if not all_finished:
            return

        time_end = time.time()
        print('time cost', time_end - time_start, 's')
        # set the state to already inited
        kv_entry = models.KvStore()
        kv_entry.field_name = STATE_FIELD_NAME
        kv_entry.field_value = STATE_FIELD_STARTED_VALUE
        session.add(kv_entry)
        session.commit()
