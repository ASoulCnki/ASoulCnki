import time

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

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
                dynamic_in_database = check_dynamic_already_exists(session, dynamic)
                if dynamic_in_database is not None:
                    dynamic_in_database.ctime = reply_tuple[3]
                    session.add(dynamic_in_database)
                    session.commit()
                    continue
                dynamic.type_id = reply_tuple[1]
                dynamic.oid = reply_tuple[2]
                dynamic.ctime = reply_tuple[3]
                dynamic.status = 0
                session.add(dynamic)
                session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            return False
        result += tuples
        if has_more == 0:
            break

    time_end = time.time()
    print("finished crawl dynamics for member {}, cost {}".format(member_id, time_end - time_start))
    return True


def check_dynamic_already_exists(session, dynamic: models.UserDynamic):
    dynamic_class = models.UserDynamic
    try:
        re = session.query(dynamic_class).filter(
            or_(dynamic_class.dynamic_id == dynamic.dynamic_id, dynamic_class.oid == dynamic.oid)).one()
        return re
    except NoResultFound:
        return None
    except MultipleResultsFound:
        return None


if __name__ == '__main__':
    asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094, 703007996]
    for member_id in asoul_member_ids:
        create_requests_and_save_data(member_id)
