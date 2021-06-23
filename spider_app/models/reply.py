from sqlalchemy import Column, TEXT, String, BIGINT, Integer

from spider_app.models.base import Base


class Reply(Base):
    # 表的名字:
    __tablename__ = 'reply'
    # 表的结构:
    rpid = Column(BIGINT, primary_key=True)
    type_id = Column(Integer)
    mid = Column(Integer)
    oid = Column(BIGINT)
    ctime = Column(Integer)
    m_name = Column(String(255))
    content = Column(TEXT)
    like_num = Column(Integer)
    json_text = Column(TEXT)
