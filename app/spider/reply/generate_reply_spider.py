from app.config import sqla
import datetime
import app.models as models
import tasks


def send_low_priority_reply_spider_task():
    session = sqla['session']
    three_day_ago = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp())
    low_priority_reply_task = session.query(models.UserDynamic).distinct(models.UserDynamic.oid).filter(
        models.UserDynamic.ctime < three_day_ago).all()
    for dynamic in low_priority_reply_task:
        param_tuple = (dynamic.type_id, dynamic.oid, dynamic.status, dynamic.dynamic_id, dynamic.uid)
        tasks.get_reply_data_task.apply_async(param_tuple, queue="reply_task_low_priority", routing_key='reply_low')


def send_high_priority_reply_spider_task():
    session = sqla['session']

    three_day_ago = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp())
    high_priority_reply_task = session.query(models.UserDynamic).distinct(models.UserDynamic.oid).filter(
        models.UserDynamic.ctime >= three_day_ago).all()
    for dynamic in high_priority_reply_task:
        param_tuple = (dynamic.type_id, dynamic.oid, dynamic.status, dynamic.dynamic_id, dynamic.uid)
        tasks.get_reply_data_task.apply_async(param_tuple, queue="reply_task_high_priority", routing_key='reply_high')


if __name__ == '__main__':
    send_low_priority_reply_spider_task()
