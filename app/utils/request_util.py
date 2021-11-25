from requests import get
from app.config.secure import proxy
from .proxy import ProxyPool
# Disable SSL Verify Warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def is_valid_proxy(proxy):
    # 判断代理格式是否正确
    if not (type(proxy) == type({})):
        return {}
    return proxy


isNotNullProxy = True if is_valid_proxy(proxy) == {} else False

proxyPool = ProxyPool(proxyConfig=proxy, interval=isNotNullProxy)


def url_get(url, mode=None, timeout=20, count=0):
    # 重试次数
    retry_count = count
    # 从代理池获取
    proxies = proxyPool.get()
    try:
        response = get(url=url, timeout=timeout, proxies=proxies, verify=False)
        if mode is None:
            return response
        elif mode == "json":
            return response.json()
        elif mode == "content":
            return response.content
        elif mode == "text":
            return response.text
        elif mode == "code":
            return response.status_code
        else:
            raise ValueError(
                "Mode error, mode must be one of None/json/content/text/code")
    except Exception as err:
        print(err)
        if retry_count > 3:
            # 切换到直连
            proxyPool.setDirect()
            raise Exception("Maximum retries")
        else:
            url_get(url=url, mode=mode, count=retry_count+1)


def dict_get(dict_, obj_key):
    """
    从嵌套的字典中拿到需要的值
    :param dict_: 要遍历的字典
    :param obj_key: 目标key
    :return: 目标key对应的value
    """
    if isinstance(dict_, dict):
        for key, value in dict_.items():
            if key == obj_key:
                return value
            else:
                # 如果value是dict类型，则进行迭代
                if isinstance(value, dict):
                    ret = dict_get(value, obj_key)
                    if ret is not None:
                        return ret
                # 如果value是list类型，则依次进行迭代
                elif isinstance(value, list):
                    for i in range(len(value)):
                        ret = dict_get(value[i], obj_key)
                        if ret is not None:
                            return ret
        # 如果找不到指定的key，返回None
        return None
    else:
        return None
