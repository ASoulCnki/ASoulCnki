from datetime import datetime
from urllib.parse import urlparse

from gevent.lock import BoundedSemaphore


class Throttle:
    def __init__(self, delay):
        self.domains = {}  # 可以放到数据库中
        self.delay = delay  # 两次间隔下载间隔
        self.sem = BoundedSemaphore()

    def wait_url(self, url_str):
        # 以netloc为基础进行休眠
        self.sem.acquire()
        domain_url = urlparse(url_str).netloc
        last_accessed = self.domains.get(domain_url)  # 根据字典键获取值

        if self.delay > 0 and last_accessed is not None:
            # 计算当前时间和上次访问时间段间隔，然后被规则时间减去，如果大于0，说明间隔时间不到，要继续休眠，否则的话直接下载下个网页
            sleep_interval = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_interval > 0:
                import time
                time.sleep(sleep_interval)

        self.domains[domain_url] = datetime.now()
        self.sem.release()
