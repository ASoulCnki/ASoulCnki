from sqlalchemy import Column, Integer, BIGINT

from app.models.base import Base


class UserDynamic(Base):
    # 表的名字:
    __tablename__ = 'user_dynamic'

    # 表的结构:
    # 动态id
    dynamic_id = Column(BIGINT, primary_key=True)
    type_id = Column(Integer)
    oid = Column(BIGINT)
    # 用户uid
    uid = Column(Integer)
    # 爬取状态
    status = Column(Integer)
    ctime = Column(Integer)
