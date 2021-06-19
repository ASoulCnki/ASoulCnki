from kombu import Exchange, Queue

# 定义数据库信息
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义celery信息
BROKER_URL = "redis://:1234@localhost:6379/0"
BACKEND_URL = "redis://:1234@localhost:6379/1"
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_QUEUES = (
    Queue('login_queue', exchange=Exchange('login', type='direct'), routing_key='for_login'),
    Queue('fans_followers', exchange=Exchange('fans_followers', type='direct'), routing_key='for_fans_followers'),
)
