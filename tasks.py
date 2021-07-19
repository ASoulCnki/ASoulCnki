import os
import time

import socket
from app.config import celery_app
from app.lib import send_mail
from app.spider import dynamic, reply


@celery_app.task
def get_dynamic_full_data_task(member_ids):
    return dynamic.get_dynamic_full_data.task(member_ids)


@celery_app.task
def get_dynamic_base_data_task(member_ids):
    return dynamic.get_dynamic_base_data.task(member_ids)


@celery_app.task
def generate_low_priority_reply_spider_task():
    try:
        reply.generate_reply_spider.send_low_priority_reply_spider_task()
    except Exception as e:
        send_mail("high priority reply task error, host:{}  error: {}".format(socket.gethostname(), e))
        os.system("bash stop.sh")


@celery_app.task
def generate_high_priority_reply_spider_task():
    try:
        reply.generate_reply_spider.send_high_priority_reply_spider_task()
    except Exception as e:
        send_mail("high priority reply task error, host:{}  error: {}".format(socket.gethostname(), e))
        os.system("bash stop.sh")


@celery_app.task
def get_reply_data_task(type_id, oid, status, dynamic_id):
    try:
        reply.get_reply_data.task(type_id, oid, status, dynamic_id)
    except Exception as e:
        send_mail("get reply task error, host:{}  error: {}".format(socket.gethostname(), e))
        os.system("bash stop.sh")


@celery_app.task
def pull_data_task():
    try:
        import datetime
        one_day_ago = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())
        reply.pull_data.task(one_day_ago)
    except Exception as e:
        send_mail("get reply task error, host:{}  error: {}".format(socket.gethostname(), e))
        os.system("bash stop.sh")


@celery_app.task
def refresh_like_num_task(type_id, oid, dynamic_id, min_time):
    try:
        reply.refresh_like_num.task(type_id, oid, dynamic_id, min_time)
    except Exception as e:
        send_mail("get reply task error, host:{}  error: {}".format(socket.gethostname(), e))
        os.system("bash stop.sh")


@celery_app.task
def generate_refresh_like_num_task():
    try:
        import datetime
        one_week_ago = int((datetime.datetime.now() - datetime.timedelta(weeks=1)).timestamp())
        reply.generate_refresh_like_spider.send_refresh_like_spider(one_week_ago)
    except Exception as e:
        send_mail("refresh like num task error, host:{}  error: {}".format(socket.gethostname(), e))
        os.system("bash stop.sh")


@celery_app.task
def raise_exception():
    try:
        raise ValueError("error")
    except Exception as e:
        print(e)
        raise_exception.delay()
        time.sleep(1)
        os.system("sh stop.sh")


@celery_app.task
def send_stats_email():
    reply.stats.get_stats()
