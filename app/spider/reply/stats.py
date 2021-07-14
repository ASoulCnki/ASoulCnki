from app import models
import datetime
from app.config import sqla
from app.lib import send_mail


def get_stats():
    session = sqla['session']
    one_day_ago = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())
    all_reply_count = session.query(models.Reply).count()
    today_reply_count = session.query(models.Reply).filter(models.Reply.ctime > one_day_ago).count()
    all_dynamic_count = session.query(models.UserDynamic).count()
    today_dynamic_count = session.query(models.UserDynamic).filter(models.UserDynamic.ctime > one_day_ago).count()
    uninited_dynamic_count = session.query(models.UserDynamic).filter(models.UserDynamic.status == 0).count()
    email_content = "总评论数: {} \n今日爬取评论数: {}\n\n 总动态数: {} \n今日爬取动态数: {}\n 未爬取动态数: {}".format(all_reply_count,
                                                                                            today_reply_count,
                                                                                            all_dynamic_count,
                                                                                            today_dynamic_count,
                                                                                            uninited_dynamic_count)
    send_mail(email_content, title="枝网查重统计数据")


if __name__ == '__main__':
    get_stats()
