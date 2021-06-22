# -*- encoding: utf-8 -*-
'''
Filename         :check.py
Description      :查重算法实现
Time             :2021/06/22 15:52:02
Author           :hwa
Version          :1.0
'''
from typing import Counter
from hash import hash

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
    with open("database.dat","rb") as f:
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
            if text_hash in article[1] and text_hash not in find_list:
                if article[0] not in count_dict:
                    count_dict[article[0]]=1
                else:
                    count_dict[article[0]]+=1
                count_all+=1
                find_list.append(text_hash)
    sorted_list = sorted(count_dict.items(), key=lambda item:item[1], reverse=True)
    rate = count_all/len(text_hash_list)
    return rate, sorted_list[:n]
def test():
    text = """大家好，我是bilibili用户。
十分感谢大家一直以来的支持。
最近由于本人精神状态的不稳定及措辞不当，说了很多攻击乐华公司和其粉丝的话，对此我真的非常抱歉。
而我自己，目前正处于想要尽快打起精神而着急采取行动的状态中。出于以上的考虑，我将停止包括百度贴吧，bilibili，nga在内的全平台攻击乐华公司的活动，进行维持一周左右的自肃，还请大家给我一段整理心情的时间。并允许我在复播的时候，于bilibili限定和nga专楼中向乐华公司的粉丝进行正式的道歉。
在我过往的anti中遭遇困难的时候，持续支持鼓励我的大家，以及现在还在攻击乐华公司和其粉丝的人们，我只能说你们好自为之。非常感谢你们。
希望粉丝能够信任我并原谅我。
    """
    print(check(text, 5))

if __name__=="__main__":
    test()