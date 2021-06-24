from sqlalchemy import Column, TEXT, String, BIGINT, Integer

from app.models.base import Base


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

    def keys(self):
        return ['rpid', 'type_id', 'mid', 'oid', 'ctime', 'm_name', 'content', 'like_num']

    def __getitem__(self, item):
        return getattr(self, item)
