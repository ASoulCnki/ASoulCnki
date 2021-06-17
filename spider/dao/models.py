from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 定义 Player 对象:
class UserDynamic(Base):
    # 表的名字:
    __tablename__ = 'user_dynamic'

    # 表的结构:
    dynamic_id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    oid = Column(Integer)
