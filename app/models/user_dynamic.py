from sqlalchemy import Column, Integer

from app.models.base import Base


class UserDynamic(Base):
    # 表的名字:
    __tablename__ = 'user_dynamic'

    # 表的结构:
    # 动态id
    dynamic_id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    oid = Column(Integer)
    # 爬取状态
    status = Column(Integer)
