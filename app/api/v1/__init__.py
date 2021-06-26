from flask import Blueprint
from app.api.v1 import reply_duplicaion_check
from app.api.v1 import reply_source


def create_blueprint_v1():
    bp_v1 = Blueprint("v1", __name__, url_prefix="/")

    reply_duplicaion_check.api.register(bp_v1)
    reply_source.api.register(bp_v1)
    # add more api
    return bp_v1
