from app.config import sqla
import app.models as models
import tasks


def send_low_priority_reply_spider_task():
    session = sqla['session']
    inited_dynamics = session.query(models.UserDynamic).filter(models.UserDynamic.status == 1).all()
    for dynamic in inited_dynamics:
        param_tuple = (dynamic.type_id, dynamic.oid, dynamic.status, dynamic.dynamic_id)
        tasks.get_reply_data_task.apply_async(param_tuple, queue="reply_task_low_priority")


def send_high_priority_reply_spider_task():
    session = sqla['session']

    un_inited_dynamics = session.query(models.UserDynamic).filter(models.UserDynamic.status == 0).all()
    for dynamic in un_inited_dynamics:
        param_tuple = (dynamic.type_id, dynamic.oid, dynamic.status, dynamic.dynamic_id)
        tasks.get_reply_data_task.apply_async(param_tuple, queue="reply_task_low_priority")
        tasks.get_reply_data_task.delay(param_tuple)
