# -*- encoding: utf-8 -*-
"""
Filename         :check.py
Description      :查重算法实现
Time             :2021/06/22 15:52:02
Author           :hwa
Version          :1.0
"""
import time

from app.lib.duplication_check.compare import article_compare
from app.lib.duplication_check.hash import hash
from app.lib.duplication_check.reply_database import ReplyDatabase
from app.lib.duplication_check.reply_model import Reply


def get_database():
    """
    TODO:整合数据库
    @description  :
    获取摘要数据库
    @param  :
    @Returns  :
    摘要数据列表[("唯一id",[摘要]),...]
    """
    import os
    return ReplyDatabase.load_from_image("database.dat")


def check(database: ReplyDatabase, text, n):
    text_hash_list = hash(text)
    count_dict = {}
    find_set = set()

    hits = 0

    for text_hash in text_hash_list:
        text_hash_optional = database.search_hash(text_hash)
        if text_hash_optional:
            for item in text_hash_optional:
                if item not in count_dict:
                    count_dict[item] = 1
                else:
                    count_dict[item] += 1
            if text_hash not in find_set:
                find_set.add(text_hash)
                hits += 1

    sorted_list = sorted(count_dict.items(), key=lambda item: item[1], reverse=True)[:n]

    result = []
    all_content = ""
    for item in sorted_list:
        reply = database.get_reply(item[0])
        content = reply.content
        hit = article_compare(text, content)
        similarity = hit / len(text)
        if similarity < 0.3:
            continue
        all_content += content
        result.append((similarity, reply, get_reply_url(reply)))
    all_similarity = article_compare(text, all_content) / len(text)
    return result, text, all_similarity


def get_reply_url(reply: Reply):
    base_url = "https://www.bilibili.com"
    dynamic_base_url = "https://t.bilibili.com"
    if reply.type_id == 1:
        return "{}/video/av{}/#reply{}".format(base_url, reply.oid, reply.rpid)
    elif reply.type_id == 17 or reply.type_id == 11:
        return "{}/{}/#reply{}".format(dynamic_base_url, reply.dynamic_id, reply.rpid)


def test():
    start_time = time.time()
    database = get_database()
    cost = time.time() - start_time
    print("load database cost {} s".format(cost))

    start_time = time.time()
    count = 0
    max_query = 100
    final_result = []
    for reply in database.reply_dict.values():
        reply_content = reply.content
        if len(reply_content) < 300:
            continue

        count += 1
        if count == max_query:
            break
        final_result.append(check(database, reply_content, 5))
    cost = time.time() - start_time
    print("query {} records , total cost {} s, in average {} s ".format(max_query, cost, cost / max_query))
    for result in final_result:
        similar_text_list = result[0]
        if len(similar_text_list) == 0:
            continue
        print("text: {}, all_similarity: {}".format(result[1], result[2]))
        # for similar_text in similar_text_list:
        #     print("similarity: {}, content {}".format(similar_text[0], similar_text[1].content))


if __name__ == "__main__":
    test()
    # text = """
    #     """
    # db = get_database()
    # r = check(db, text, 5)
    # for t in r:
    #     print("similarity: {}, content {}".format(t[0], t[1]))
