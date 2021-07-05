import os
import time

from app.config import celery_app
from app.spider import dynamic, reply


@celery_app.task
def get_dynamic_full_data_task(member_ids, pool_num):
    return dynamic.get_dynamic_full_data.task(member_ids, pool_num)


@celery_app.task
def get_dynamic_base_data_task(member_ids, pool_num):
    return dynamic.get_dynamic_base_data.task(member_ids, pool_num)


@celery_app.task
def generate_reply_spider_task(un_inited_only):
    return reply.generate_reply_spider.task(un_inited_only)


@celery_app.task
def get_reply_data_task(tuples, pool_num):
    try:
        reply.get_reply_data.task(tuples, pool_num)
    except Exception as e:
        print(e)
        get_reply_data_task(tuples, pool_num).delay()
        os.system("sh stop.sh")


@celery_app.task
def print_alive():
    print("I am still alive")


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
