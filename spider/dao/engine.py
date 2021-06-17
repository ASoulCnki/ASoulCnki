from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from secure import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
