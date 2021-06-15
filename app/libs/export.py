from sqlalchemy import asc, desc
from xlwt.Worksheet import Worksheet

from app.models.base import db
from app.models.camp_models.course_contest import CourseContest
from app.models.camp_models.course_oj_username import CourseOJUsername
from app.models.camp_models.user_contest import UserContest
from app.models.user import User


def query_course_rating(course_id):
    res = db.session.query(CourseOJUsername, UserContest, CourseContest). \
        filter(UserContest.contest_id == CourseContest.id,
               CourseOJUsername.course_id == CourseContest.course_id,
               CourseOJUsername.username == UserContest.username). \
        filter(CourseOJUsername.course_id == course_id). \
        group_by(CourseOJUsername.oj_username, UserContest.contest_id). \
        order_by(asc(UserContest.contest_id), desc(UserContest.rating)).all()
    info = {}
    for i, j, k in res:
        info.setdefault(k.name, {})
        info[k.name].update({i.oj_username: j.rating})
    return info


def teams2user(course_id):
    res = {}
    course_oj_usernames = CourseOJUsername.search(course_id=course_id, page_size=-1)['data']
    for course_oj_username in course_oj_usernames:
        oj_username = course_oj_username.oj_username
        res.setdefault(oj_username, [])
        username = course_oj_username.username
        nickname = User.get_by_id(username).nickname
        res[oj_username].append(nickname)
    return res


def export_to_sheet(sheet: Worksheet, course_id):
    info = query_course_rating(course_id)
    res = {}
    courses = set()
    for course_name, ratings in info.items():
        courses.add(course_name)
        for team_name, rating in ratings.items():
            res.setdefault(team_name, {'total': 0})
            res[team_name][course_name] = rating
            res[team_name]['total'] += rating
    courses = sorted(list(courses), key=lambda x: (len(x), x))
    for i in res.keys():
        res[i]['total'] = round(res[i]['total'], 3)
    team2user_table = teams2user(course_id)
    res = [{
        'team_name': i,
        'members': team2user_table[i],
        'total_rating': j['total'],
        'detail': {key: val for key, val in j.items() if key != 'total'}
    } for i, j in res.items()]
    res.sort(key=lambda item: item['total_rating'], reverse=True)
    sheet.write(0, 0, '排名')
    sheet.write(0, 1, '队伍名')
    sheet.write(0, 2, '队伍成员')
    sheet.write(0, 3, '总分')
    for row, team_info in enumerate(res, 1):
        sheet.write(row, 0, row)
        sheet.write(row, 1, team_info['team_name'])
        sheet.write(row, 2, ','.join(team_info['members']))
        sheet.write(row, 3, team_info['total_rating'])
    for col, contest_name in enumerate(courses, 4):
        sheet.write(0, col, contest_name)
        for row, team_info in enumerate(res, 1):
            sheet.write(row, col, team_info['detail'].get(contest_name, 0))
