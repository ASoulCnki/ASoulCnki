# A-SOUL评论区小作文 枝网查重系统

网站地址：https://asoulcnki.asia

项目首页：https://github.com/ASoulCnki

项目后端（基于spring boot）已迁移至 https://github.com/ASoulCnki/ASoulCnkiBackend

项目前端（基于vue2）已迁移至 https://github.com/ASoulCnki/ASoulCnkiFrontend

项目新前端（基于vue3）已迁移至 https://github.com/ASoulCnki/ASoulCnkiFrontendV3

本项目为枝网查重的动态+评论区爬虫部分

爬虫部署文档:[Deploy.md](./Deploy.md)
## 简介


### 想法起源
#### NGA Asoul板块 
- [想搞一个asoul知网查重小作文](https://bbs.nga.cn/read.php?tid=27186618)。

#### 豆瓣相关讨论
- [一个想法，发病小作文查重系统， 来征求一下豆油的意见](https://www.douban.com/group/topic/230466414/)
- [ASoul评论区发病小作文 枝网查重系统 需求讨论楼](https://www.douban.com/group/topic/230489644/?start=0)

简单总结就是做一个A-Soul评论区的小作文数据库，并提供查重能力。让广大au可以精准甄别评论是是原偷/原创，还是从之前的评论区复制粘贴改词偷来的😈

### A-Soul 简介

A-SOUL是乐华娱乐于2020年11月23日公开的其旗下首个虚拟偶像团体，由5名成员组成。

A-SOUL主页链接：https://space.bilibili.com/703007996 <br>
乃琳：https://space.bilibili.com/672342685 <br>
珈乐：https://space.bilibili.com/351609538 <br>
嘉然：https://space.bilibili.com/672328094 <br>
贝拉：https://space.bilibili.com/672353429 <br>
向晚：https://space.bilibili.com/672346917 <br>

在未来学院中，五位性格迥异的少女，为了成为偶像这一共同目标走到一起，并且为之努力奋斗。
设定中，她们生活在虚拟城市枝江。所以系统名为枝网查重系统（化用知网）。



## Todos

一期计划开发进度:

- [x] 完成基本的动态和评论区爬虫
- [x] 基于数据库实现增量式爬虫, 近实时更新评论数据（基本完成）
- [x] 构建查重系统
- [x] 查重网站前后端

优化点：

- [x] 使用不同的celery队列放置不同的任务
- [x] 使用代理池和更合适的客户端限流策略避免被叔叔封禁ip（采取了使用较低的爬取频率的办法)
- [x] 错误处理，如被限流时更换ip，出现未知错误时邮件/短信告警（已实现邮件报警)
