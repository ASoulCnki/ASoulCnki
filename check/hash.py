# -*- encoding: utf-8 -*-
'''
Filename         :hash.py
Description      :摘要算法相关函数
Time             :2021/06/22 15:20:24
Author           :hwa
Version          :1.0
'''

def hashValue(s,k,q,b):
    num = 0
    for index, c in enumerate(s):
        num+=ord(c)*(b**(k-1-index))
    return num%q

def hash(s, k=4, q=1145141919780, b=2, w=4):
    """
    @description  :
    对字符串做摘要
    @param  :
    s: 字符串
    k: 敏感度 即几个字做一次摘要
    q: 模数 摘要结果对其取模
    b: 基数 摘要算法的基数
    w: 窗口宽度 选择摘要时的窗口大小
    @Returns  :
    字符串的摘要
    """
    # 逐位做摘要
    hash=[]
    hash.append(hashValue(s[:k],k,q,b))
    for i in range(1, len(s)-k+1):
        hash.append(hashValue(s[i:k+i],k,q,b))
    # 选择摘要
    hash_pick=[]
    hash_pick.append(min(hash[:w]))
    j = 1
    while(j+w<=len(hash)):
        min_hash = min(hash[j:j+w])
        if min_hash!=hash_pick[-1]:
            hash_pick.append(min_hash)
        j+=1
    return hash_pick