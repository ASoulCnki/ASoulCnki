from app import models
from app.config import sqla
from app.spider.reply.reply_spider import crawl_reply_once


def create_request_and_save_data(type_id, oid, dynamic_id, min_time):
    session = sqla['session']

    page_size = 49
    next_offset = 0
    finished = False
    while not finished:
        try:
            is_end, next_offset, result = crawl_reply_once(oid, type_id, dynamic_id, page_size, next_offset)
            for reply in result:
                # we only process replies after ctime
                if reply.ctime < min_time:
                    return
                old_reply = session.query(models.Reply).filter(models.Reply.rpid == reply.rpid).one_or_none()
                if old_reply is None:
                    session.add(reply)
                    session.commit()
                else:
                    if old_reply.like_num != reply.like_num:
                        session.query(models.Reply).filter(models.Reply.rpid == reply.rpid).update(
                            {"like_num": reply.like_num})
                        session.commit()
            if is_end:
                break
        except Exception as e:
            session.rollback()
            raise e


def task(type_id, oid, dynamic_id, min_time):
    create_request_and_save_data(type_id, oid, dynamic_id, min_time)


if __name__ == '__main__':
    create_request_and_save_data(17, 536180349987980387, 536180349987980387, 1623686400)
