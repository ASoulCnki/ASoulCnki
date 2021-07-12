import os
import time

from app.config import celery_app
from app.spider import dynamic, reply


@celery_app.task
def get_dynamic_full_data_task(member_ids):
    return dynamic.get_dynamic_full_data.task(member_ids)


@celery_app.task
def get_dynamic_base_data_task(member_ids):
    return dynamic.get_dynamic_base_data.task(member_ids)


@celery_app.task
def generate_low_priority_reply_spider_task():
    return reply.generate_reply_spider.send_low_priority_reply_spider_task()


@celery_app.task
def generate_high_priority_reply_spider_task():
    return reply.generate_reply_spider.send_high_priority_reply_spider_task()


@celery_app.task
def get_reply_data_task(type_id, oid, status, dynamic_id):
    try:
        reply.get_reply_data.task(type_id, oid, status, dynamic_id)
    except Exception as e:
        print(e)
        get_reply_data_task(type_id, oid, status, dynamic_id).apply_async((type_id, oid, status, dynamic_id),
                                                                          countdown=60 * 10)
        os.system("sh stop.sh")


@celery_app.task
def pull_data_task():
    import datetime
    one_day_ago = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())
    return reply.pull_data.task(one_day_ago)


@celery_app.task
def raise_exception():
    try:
        raise ValueError("error")
    except Exception as e:
        print(e)
        raise_exception.delay()
        time.sleep(1)
        os.system("sh stop.sh")
