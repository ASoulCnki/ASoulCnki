import requests

from app.config.secure import CONTROL_SECURE_KEY, base_url


def task(start_time):
    r = requests.post(base_url,
                      json={'secure_key': CONTROL_SECURE_KEY, 'start_time': start_time})
    print(r.json())


if __name__ == '__main__':
    import datetime

    one_day_ago = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())
    task(one_day_ago)
