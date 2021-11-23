# timer
from threading import Timer
from requests import get


class ProxyPool():

    def __init__(self, proxyConfig, interval=True, intervalRange=60):
        '''
        @param proxyConfig: like proxies in requests.get()
        @param interval: start interval
        @param intervalRange: interval range of timer (seconds), default is 60s
        '''
        self.proxyConfig = proxyConfig
        self.nowProxy = {}
        self.intervalRange = intervalRange
        if (interval):
            Timer(intervalRange, self.flush).start()

    def get(self):
        '''
        get now proxy, if no proxy, return {}
        '''
        return self.nowProxy

    def setDirect(self):
        '''
        when no proxy is usable, set direct
        '''
        self.nowProxy = {}

    def flush(self):

        # use requests.get() to test proxy
        def isProxyUsable():
            testUrl = 'https://baidu.com'
            try:
                get(testUrl, proxies=self.proxyConfig, timeout=5)
                return True
            except Exception:
                return False

        if isProxyUsable():
            self.nowProxy = self.proxyConfig
        else:
            self.nowProxy = {}

        Timer(self.intervalRange, self.flush).start()
