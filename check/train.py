# -*- encoding: utf-8 -*-
'''
Filename         :train.py
Description      :获取小作文摘要
Time             :2021/06/22 15:21:08
Author           :hwa
Version          :1.0
'''
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

def save_data(id, hash):
    """
    TODO:整合数据库
    @description  :
    抽象出的存储小作文摘要的接口
    @param  :
    id: 小作文的唯一id
    hash: 小作文的摘要
    @Returns  :
    """
    test_hash_data.append((id, hash))

def train():
    while True:
        data = get_data()
        if data==None:
            break
        save_data(id=data[0],hash=hash(data[1]))

# test_code
test_data_list = []
test_hash_data = []
def test():
    import os
    import pickle
    path = input("已知小作文所在文件夹:")
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                test_data_list.append((path,text))
    train()
    with open("database.dat","wb") as f:
        pickle.dump(test_hash_data, f)
if __name__=="__main__":
    test()