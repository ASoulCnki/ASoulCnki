from app.models.base import Base
from app.models.kvstore import KvStore
from app.models.user_dynamic import UserDynamic
from app.models.reply import Reply
from app.config import engine

Base.metadata.create_all(engine)
