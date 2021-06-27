import sys
from app.lib.duplication_check.train import train_data
from app.lib.duplication_check.reply_database import ReplyDatabase, reply_db_singleton
from app.lib.duplication_check.pull_data import pull_data_from_database
from tasks import (
    generate_reply_spider_task,
    get_dynamic_base_data_task,
    get_dynamic_full_data_task,
)


def init_dynamic():
    asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094]
    get_dynamic_base_data_task.delay(asoul_member_ids, 5)


def init_reply():
    generate_reply_spider_task.delay(True)


def update_database():
    asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094]
    get_dynamic_full_data_task.delay(asoul_member_ids, 5).get()
    generate_reply_spider_task.delay(False)


def pull_data(start_time):
    pull_data_from_database(reply_db_singleton, start_time)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'init_reply':
            init_reply()
        elif sys.argv[1] == 'init_dynamic':
            init_dynamic()
        elif sys.argv[1] == 'update':
            update_database()
        elif sys.argv[1] == 'train':
            train_data()
        elif sys.argv[1] == 'pull_data':
            if len(sys.argv) < 3:
                print("error param number")
                sys.exit(1)
            start_time = sys.argv[2]
            pull_data(start_time)
    else:
        print("error param number")
