from app.config import sqla
import app.models as models
import tasks


def send_reply_spider_task(un_inited_only):
    session = sqla['session']

    pool_num = 4
    if not un_inited_only:
        inited_dynamics = session.query(models.UserDynamic).filter(models.UserDynamic.status == 1).all()
        batch_size = 16
        batch_count = 0
        batch = []
        for dynamic in inited_dynamics:
            batch_count += 1
            batch.append((dynamic.type_id, dynamic.oid, dynamic.status))
            if batch_count == batch_size:
                tasks.get_reply_data_task.delay(batch, pool_num)
                batch = []
                batch_count = 0

        if batch_count > 0:
            tasks.get_reply_data_task.delay(batch, pool_num)

    un_inited_dynamics = session.query(models.UserDynamic).filter(models.UserDynamic.status == 0).all()
    for dynamic in un_inited_dynamics:
        param_tuple = (dynamic.type_id, dynamic.oid, dynamic.status)
        tasks.get_reply_data_task.delay([param_tuple], pool_num)


def task(un_inited_only):
    session = sqla['session']
    state = session.query(models.KvStore).filter(models.KvStore.field_name == 'state').all()

    # check if the database is inited, if not, do initialization
    if not len(state):
        return

    send_reply_spider_task(un_inited_only)
