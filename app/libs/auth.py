import functools

from flask_login import current_user

from app.libs.error_code import Forbidden


def admin_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.permission != 1:
            raise Forbidden()
        return func(*args, **kwargs)

    return wrapper
