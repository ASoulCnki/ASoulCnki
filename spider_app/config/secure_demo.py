from datetime import timedelta

from kombu import Exchange, Queue

# 定义数据库信息
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义celery信息
broker_url = "redis://:1234@localhost:6379/0"
result_backend = "redis://:1234@localhost:6379/1"
timezone = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
worker_prefetch_multiplier = 2
worker_concurrency = 2
worker_max_tasks_per_child = 2
