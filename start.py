import sys

from tasks import (
    generate_low_priority_reply_spider_task,
    generate_high_priority_reply_spider_task,
    get_dynamic_base_data_task,
    pull_data_task, get_dynamic_full_data_task
)

asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094, 703007996]


def init_dynamic():
    get_dynamic_base_data_task.delay(asoul_member_ids, 5)


def init_reply():
    generate_high_priority_reply_spider_task.delay()
    generate_low_priority_reply_spider_task.delay()


def update_database():
    get_dynamic_full_data_task.delay(asoul_member_ids).get()
    init_reply()


def pull_data():
    pull_data_task.delay().get()


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
    else:
        print("error param number")
