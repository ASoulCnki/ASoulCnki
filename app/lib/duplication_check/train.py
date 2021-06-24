# -*- encoding: utf-8 -*-
"""
Filename         :train.py
Description      :获取小作文摘要
Time             :2021/06/22 15:21:08
Author           :hwa
Version          :1.0
"""
from app.lib.duplication_check.reply_database import ReplyDatabase
import time


def train_data():
    start_time = time.time()
    db = ReplyDatabase.load_from_json("data/bilibili_cnki_reply.json")
    db.dump_to_image("database.dat")
    end_time = time.time()
    print("train cost {} s".format(end_time - start_time))


if __name__ == "__main__":
    train_data()
