import tasks
from app.config import sqla
from app.models import Reply


def send_refresh_like_spider(min_time):
    session = sqla['session']
    res = session.query(Reply.type_id, Reply.oid, Reply.dynamic_id,Reply.uid, min_time). \
        filter(Reply.ctime > min_time).distinct(Reply.oid).all()

    for r in res:
        param = (r[0], r[1], r[2], r[3],r[4])
        tasks.refresh_like_num_task.apply_async(param, queue="reply_task_low_priority", routing_key='reply_low')


if __name__ == '__main__':
    send_refresh_like_spider(1628092800)
