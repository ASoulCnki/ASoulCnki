from flask import Blueprint
from app.api.frontend import view


def create_blueprint_view():
    bp_view = Blueprint("view", __name__)

    view.api.register(bp_view)
    # add more api
    return bp_view
