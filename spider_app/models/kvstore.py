from sqlalchemy import Column, TEXT, String

from spider_app.models.base import Base


class KvStore(Base):
    # 表的名字:
    __tablename__ = 'kv_store'
    # 表的结构:
    field_name = Column(String(255), primary_key=True)
    field_value = Column(TEXT)
