import sys

from app.lib.mail import send_mail
from app.config.secure import member_ids
from tasks import (
    generate_low_priority_reply_spider_task,
    generate_high_priority_reply_spider_task,
    get_dynamic_base_data_task,
    pull_data_task, get_dynamic_full_data_task,
    raise_exception
)

asoul_member_ids = member_ids


def init_dynamic():
    get_dynamic_base_data_task.delay(asoul_member_ids)


def init_reply():
    generate_high_priority_reply_spider_task.delay()
    generate_low_priority_reply_spider_task.delay()


def update_database():
    get_dynamic_full_data_task.delay(asoul_member_ids).get()
    init_reply()
    pull_data()


def pull_data():
    pull_data_task.delay()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'init_reply':
            init_reply()
        elif sys.argv[1] == 'init_dynamic':
            init_dynamic()
        elif sys.argv[1] == 'update':
            update_database()
        elif sys.argv[1] == 'pull_data':
            pull_data()
        elif sys.argv[1] == 'send_mail':
            send_mail("hello")
        elif sys.argv[1] == 'kill':
            raise_exception()

    else:
        print("error param number")
