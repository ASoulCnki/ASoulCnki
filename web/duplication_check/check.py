# -*- encoding: utf-8 -*-
"""
Filename         :check.py
Description      :查重算法实现
Time             :2021/06/22 15:52:02
Author           :hwa
Version          :1.0
"""
import time

from .compare import article_compare
from .hash import hash


def get_database():
    """
    TODO:整合数据库
    @description  :
    获取摘要数据库
    @param  :
    @Returns  :
    摘要数据列表[("唯一id",[摘要]),...]
    """
    import pickle
    with open("database.dat", "rb") as f:
        hash_data = pickle.load(f)
    return hash_data


def check(text, n):
    """
    @description  :
    查重算法实现
    @param  :
    text: 待查重文本
    @Returns  :
    重复率
    n篇最相似的小作文
    """
    text_hash_list = hash(text)
    count_dict = {}
    count_all = 0
    find_list = []
    database = get_database()
    for article in database:
        for text_hash in text_hash_list:
            if text_hash in article[1]:
                if article[0] not in count_dict:
                    count_dict[article[0]] = 1
                else:
                    count_dict[article[0]] += 1
                if text_hash not in find_list:
                    count_all += 1
                    find_list.append(text_hash)
    sorted_list = sorted(count_dict.items(), key=lambda item: item[1], reverse=True)
    rate = count_all / len(text_hash_list)
    return rate, sorted_list[:n]


def check_v2(database, text, n):
    text_hash_dict = database["hash_dict"]
    reply_dict = database["reply_dict"]

    text_hash_list = hash(text)
    count_dict = {}
    find_set = set()

    hits = 0

    for text_hash in text_hash_list:
        if text_hash in text_hash_dict:
            for item in text_hash_dict[text_hash]:
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
        content = reply_dict[item[0]][0]
        hit = article_compare(text, content) 
        similarity = hit / len(text)
        if similarity < 0.3:
            continue
        all_content+=content
        result.append((similarity, content))
    result.append((article_compare(text, all_content) / len(text), text))
    return result


def test_v2():
    start_time = time.time()
    database = get_database()
    cost = time.time() - start_time
    print("load database cost {} s".format(cost))

    start_time = time.time()
    count = 0
    max_query = 100
    final_result = []
    for reply in database["reply_dict"].values():
        text = reply[0]
        if len(text) < 300:
            continue

        count += 1
        if count == max_query:
            break
        final_result.append(check_v2(database, text, 5))
    cost = time.time() - start_time
    print("query {} records , total cost {} s, in average {} s ".format(max_query, cost, cost / max_query))
    for result in final_result:
        if result is None or len(result) == 0:
            continue
        print("text: {}".format(result[0][2]))
        for t in result:
            print("similarity: {}, content {}".format(t[0], t[1]))


def test():
    text = """大家好，我是bilibili用户。
十分感谢大家一直以来的支持。
最近由于本人精神状态的不稳定及措辞不当，说了很多攻击乐华公司和其粉丝的话，对此我真的非常抱歉。
而我自己，目前正处于想要尽快打起精神而着急采取行动的状态中。出于以上的考虑，我将停止包括百度贴吧，bilibili，nga在内的全平台攻击乐华公司的活动，进行维持一周左右的自肃，还请大家给我一段整理心情的时间。并允许我在复播的时候，于bilibili限定和nga专楼中向乐华公司的粉丝进行正式的道歉。
在我过往的anti中遭遇困难的时候，持续支持鼓励我的大家，以及现在还在攻击乐华公司和其粉丝的人们，我只能说你们好自为之。非常感谢你们。
希望粉丝能够信任我并原谅我。
    """
    print(check(text, 5))


if __name__ == "__main__":
    # test()
    test_v2()
#     text = """亵渎乃琳的人有难了，因为乃琳的国将对他紧闭！
# 计量乃琳的人有难了，因为他也必在永火之中被计量！
# 为至高者排序的人有难了，因为怜悯在不敬者的头上是黯淡的，乃琳也必将其排在忠诚的粉丝之后！
# 我见兽从雪山中来，有二角一尾，在角上戴着十个冠冕，头上有亵渎的名号。造谣的人都跟从那兽，又拜它作皇，因为有权柄赐他，可以说造谣淫秽话的口，兽就开口亵渎乃琳的名并牠的帐幕。牠必折磨至高者的粉丝，逼迫他们背反乃琳的诫命。牠必在众人前行异事，好夸大她的微小，以迷惑5ch和V8的蒙昧者追随牠，将牠捧到高云之上，称作人之国的王。牠又召集众人，不论贫富老幼，刻下兽的印记，并赐给权柄，与牠一并说淫秽的话，亵渎乃琳所称的义，贬损她的名。凡有智慧的，可以计算兽印的轮廓。因为那是众人的数目，它的形状是?。
# 他领受了权柄可肆意妄行二十四个月，但在期满后我又见一位天使站在海上手持锁链将兽擒拿，让她从天上坠落，而那些被兽迷惑领受了印的，行奇事的，将乃琳排在兽后的也同被擒拿，他们被投入v8的粪坑中，天狗饱食了他们的肉。
#         """
#     database = get_database()
#     print()
#     r = check_v2(database, text, 5)
#     for t in r:
#         print("similarity: {}, content {}".format(t[0], t[1]))
