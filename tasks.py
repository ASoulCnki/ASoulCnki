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
    return reply.get_reply_data.task(tuples, pool_num)
