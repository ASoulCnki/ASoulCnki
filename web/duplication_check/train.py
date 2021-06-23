# -*- encoding: utf-8 -*-
"""
Filename         :train.py
Description      :获取小作文摘要
Time             :2021/06/22 15:21:08
Author           :hwa
Version          :1.0
"""
import json
import time

from hash import hash


def get_data():
    """
    TODO:整合数据库
    @description  :
    抽象出的获取小作文的接口，获取小作文内容。返回不为空时会继续训练
    @param  :
    @Returns  :
    ("小作文唯一id","小作文内容")
    """
    if test_data_list:
        return test_data_list.pop()
    else:
        return None


def save_data(rpid, hash_val):
    """
    TODO:整合数据库
    @description  :
    抽象出的存储小作文摘要的接口
    @param  :
    id: 小作文的唯一id
    hash_val: 小作文的摘要
    @Returns  :
    """
    test_hash_data.append((rpid, hash_val))


def train():
    while True:
        data = get_data()
        if data is None:
            break
        save_data(rpid=data[0], hash_val=set(hash(data[1])))  # 使用set替换list能大幅度提升查找速度


# test_code
test_data_list = []
test_hash_data = []


def load_json_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
        replies = []
        for reply_dict in load_dict:
            replies.append((reply_dict["rpid"], reply_dict["content"], reply_dict["ctime"]))
        return replies


def train_v2(replies):
    import pickle
    text_hash_dict = {}
    reply_dict = {}

    for reply in replies:
        # this part can be replaced by database
        reply_dict[reply[0]] = (reply[1], reply[2])

        text_hash_list = hash(reply[1])
        for text_hash in text_hash_list:
            if text_hash not in text_hash_dict:
                text_hash_dict[text_hash] = []
            text_hash_dict[text_hash].append(reply[0])
    print(text_hash_dict)
    data_store = {
        "hash_dict": text_hash_dict,
        "reply_dict": reply_dict
    }
    with open("database.dat", "wb") as f:
        pickle.dump(data_store, f)


def test():
    import os
    import pickle
    path = input("已知小作文所在文件夹:")
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                test_data_list.append((path, text))
    train()
    with open("database.dat", "wb") as f:
        pickle.dump(test_hash_data, f)


if __name__ == "__main__":
    start_time = time.time()
    result = load_json_data("./data/bilibili_cnki_reply.json")
    train_v2(result)
    end_time = time.time()
    print("train cost {} s".format(end_time - start_time))
