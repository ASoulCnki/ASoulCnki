# -*- encoding: utf-8 -*-
"""
Filename         :compare.py
Description      :1:1文章比较
Time             :2021/06/22 22:54:18
Author           :hwa
Version          :1.0
"""


def article_compare(article1, article2):
    red_list = []
    for i in range(0, len(article1)):
        if article1[i:i + 3] in article2:
            red_list = red_list + [i, i + 1, i + 2, i + 3]
    count = 0
    for index, c in enumerate(article1):
        if index in red_list:
            # print("\033[31m" + c + "\033[0m", end="")
            count += 1
        # else:
            # print(c, end="")
    return count
