from app import models
from app.config import sqla
from app.lib.duplication_check.reply_database import ReplyDatabase
from sqlalchemy import func

from app.lib.duplication_check.reply_model import Reply


def pull_data_from_database(db: ReplyDatabase, start_time):
    start_rpid = get_min_start_rpid(start_time)
    session = sqla["session"]
    page_index = 1
    page_size = 20000
    while True:
        result = session.query(models.Reply).filter(models.Reply.rpid > start_rpid).limit(page_size).offset(
            (page_index - 1) * page_size).all()
        print("pull 20000 records from database! max id: {}".format(db.max_rpid))
        if len(result) != 0:
            with db.lock.gen_wlock():
                for r in result:
                    r_for_reply_dict = Reply()
                    r_for_reply_dict.rpid = r.rpid
                    r_for_reply_dict.dynamic_id = r.dynamic_id
                    r_for_reply_dict.oid = r.oid
                    r_for_reply_dict.mid = r.mid
                    r_for_reply_dict.m_name = r.m_name
                    r_for_reply_dict.ctime = r.ctime
                    r_for_reply_dict.type_id = r.type_id
                    r_for_reply_dict.content = r.content
                    db.add_reply_data(r_for_reply_dict)
            page_index += 1
        else:
            break
    db.dump_to_image("database.dat")


def get_min_start_rpid(start_time):
    session = sqla["session"]
    try:
        start_rpid = session.query(func.min(models.Reply.rpid)).filter(models.Reply.ctime > start_time).one()[0]
        print("start pid: {}".format(start_rpid))
    except Exception:
        start_rpid = 0
    return start_rpid
