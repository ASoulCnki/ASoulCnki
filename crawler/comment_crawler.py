import re
import sys
import time

import requests


class Bilibili:
    def __init__(self, videourl, page):
        self.baseurl = videourl.split('?')[0]
        self.page = page

    # 爬取弹幕和评论
    def getAidAndCid(self):
        cidurl = self.baseurl + "?p=" + page
        cidRegx = '{"cid":([\d]+),"page":%s,' % (page)
        aidRegx = '"aid":([\d]+),'
        r = requests.get(cidurl)
        r.encoding = 'utf-8'
        try:
            self.cid = re.findall(cidRegx, r.text)[0]
            self.aid = re.findall(aidRegx, r.text)[int(page) - 1]
        except:
            print('视频序号输入有误，请保证序号在1到最大值之间！')
            time.sleep(3)
            sys.exit()

    def getComment(self, x, y):
        for i in range(x, y + 1):
            r = requests.get(
                'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&sort=2'.format(i, self.aid)).json()
            replies = r['data']['replies']
            print('------评论列表------')
            for reply in replies:
                print(reply['content']['message'] + '\n')


if __name__ == '__main__':
    # 视频地址
    videourl = input("请输入视频地址，例如:https://www.bilibili.com/video/BV13x41147nB\n")
    # 第n个视频
    page = input('请输入视频的序号：')
    # 图片储存路径
    start_time = time.time()
    # 实例化类
    b = Bilibili(videourl, page)
    # 获取aid和cid
    b.getAidAndCid()
    b.getComment(1, 4)
