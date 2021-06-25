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

task_queues = (
    Queue('default', routing_key='default'),
    Queue('dynamic_task', routing_key='dynamic'),
    Queue('reply_task', routing_key='reply'),
)

task_routes = {
    'tasks.generate_reply_spider_task': {'queue': 'default', 'routing_key': 'default'},
    'tasks.raise_exception': {'queue': 'default', 'routing_key': 'default'},
    'tasks.get_dynamic_full_data_task': {'queue': 'dynamic_task', 'routing_key': 'dynamic'},
    'tasks.get_dynamic_base_data_task': {'queue': 'dynamic_task', 'routing_key': 'dynamic'},
    'tasks.get_reply_data_task': {'queue': 'reply_task', 'routing_key': 'reply'},
}

beat_schedule = {
    'raise exception test': {
        'task': 'tasks.raise_exception',
        'schedule': timedelta(seconds=10),
    },

    'get newest dynamic ': {
        'task': 'tasks.get_dynamic_full_data',
        'schedule': timedelta(hours=2),
        'args': ([[672346917, 672342685, 672353429, 351609538, 672328094], 5])
    },

    'get newest reply': {
        'task': 'tasks.generate_reply_spider_task',
        'schedule': timedelta(hours=6),
        'args': False
    }
}
