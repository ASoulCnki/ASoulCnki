from flask import current_app

from app.models.accept_problem import AcceptProblem
from app.models.user import User


def submit_calculate_user_rating_task(username=None):
    from tasks import calculate_user_rating_task
    if username:
        user_list = [User.get_by_id(username)]
    else:
        user_list = User.search(status=1, page_size=-1)['data']
    for user in user_list:
        calculate_user_rating_task.delay(user.username)


def calculate_user_rating(username):
    rating = current_app.config['DEFAULT_USER_RATING']
    for i in AcceptProblem.search(username=username, order={'create_time': 'asc'}, page_size=-1)['data']:
        add_rating = calculate_user_add_rating(rating, i.problem.rating)
        i.modify(add_rating=add_rating)
        rating += add_rating
    user = User.get_by_id(username)
    user.modify(rating=rating)


def calculate_user_add_rating(user_rating, problem_rating):
    return int((problem_rating / user_rating) ** 2 * 5)
