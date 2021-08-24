from datetime import timedelta

from celery.schedules import crontab
from kombu import Queue

CONTROL_SECURE_KEY = "1234"
# 爬取用户id
member_ids = [672346917, 672342685, 672353429, 351609538, 672328094, 703007996]

# 后端地址
base_url = "https://asoulcnki.asia/v1/api/data/pull"

# 定义数据库信息
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[username]:[password]@[host]:[port]/[database]"
SQLALCHEMY_TRACK_MODIFICATIONS = False

mail_host = "smtp.163.com"
mail_sender = "xxx@163.com"
mail_license = "xxx"
mail_receivers = ["xxx@163.com"]

# 定义celery信息
broker_url = "redis://:[password]@[host]:[port]/0"
result_backend = "redis://:[password]@[host]:[port]/1"
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
    Queue('reply_task_high_priority', routing_key='reply_high'),
    Queue('reply_task_low_priority', routing_key='reply_low'),
)

task_routes = {
    'tasks.generate_low_priority_reply_spider_task': {'queue': 'default', 'routing_key': 'default'},
    'tasks.generate_high_priority_reply_spider_task': {'queue': 'default', 'routing_key': 'default'},
    'tasks.generate_refresh_like_num_task': {'queue': 'default', 'routing_key': 'default'},
    'tasks.raise_exception': {'queue': 'default', 'routing_key': 'default'},
    'tasks.get_dynamic_full_data_task': {'queue': 'dynamic_task', 'routing_key': 'dynamic'},
    'tasks.get_dynamic_base_data_task': {'queue': 'dynamic_task', 'routing_key': 'dynamic'},
    'tasks.pull_data_task': {'queue': 'default', 'routing_key': 'default'},
    'tasks.send_stats_email': {'queue': 'default', 'routing_key': 'default'},
}

# noinspection PyRedundantParentheses
beat_schedule = {
    'get newest dynamic ': {
        'task': 'tasks.get_dynamic_full_data_task',
        'schedule': timedelta(minutes=30),
        'args': ([member_ids])
    },

    'low priority reply task': {
        'task': 'tasks.generate_low_priority_reply_spider_task',
        'schedule': crontab(minute=0, hour='9,19'),
        'args': ([])
    },

    'high priority reply task': {
        'task': 'tasks.generate_high_priority_reply_spider_task',
        'schedule': crontab(minute=0, hour='0,3,6,9,12,15,18,21'),
        'args': ([])
    },

    'pull data': {
        'task': 'tasks.pull_data_task',
        'schedule': crontab(minute=0, hour='2,12,18,22'),
        'args': ()
    },

    'get stats': {
        'task': 'tasks.send_stats_email',
        'schedule': crontab(minute=30, hour='8'),
        'args': ()
    },

    'refresh like num': {
        'task': 'tasks.generate_refresh_like_num_task',
        'schedule': crontab(minute=0, hour='8,16'),
        'args': ([])
    },
}
