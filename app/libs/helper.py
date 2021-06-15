import datetime


def timestamp_to_str(timestamp: int) -> str:
    return datetime.datetime.strftime(
        datetime.datetime.fromtimestamp(
            timestamp, datetime.timezone(datetime.timedelta(hours=8))), '%Y-%m-%d %H:%M:%S')


def str_to_datetime(raw: str) -> datetime.datetime:
    return datetime.datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")


def datetime_to_str(raw: datetime.datetime) -> str:
    return raw.strftime("%Y-%m-%d %H:%M:%S")
