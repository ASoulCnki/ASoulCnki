from .base import Base
from .kvstore import KvStore
from .user_dynamic import UserDynamic
from app.config import engine

Base.metadata.create_all(engine)
