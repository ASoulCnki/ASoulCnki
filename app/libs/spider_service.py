import datetime

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.helper import str_to_datetime
from app.models.accept_problem import AcceptProblem
from app.models.camp_models.camp_accept_problem import CampAcceptProblem
from app.models.camp_models.camp_problem import CampProblem
from app.models.camp_models.course import Course
from app.models.camp_models.course_oj_username import CourseOJUsername
from app.models.camp_models.user_contest import UserContest
from app.models.oj import OJ
from app.models.oj_username import OJUsername
from app.models.problem import Problem
from app.models.user import User
from app.spiders.base_spider import BaseSpider
from app.spiders.camp_spiders.hdu_camp_spider import HduCampSpider
from app.spiders.camp_spiders.nowcoder_camp_spider import NowcoderCampSpider
from app.spiders.codeforces_spider import CodeforcesSpider
from app.spiders.hdu_spider import HduSpider
from app.spiders.hysbz_spider import HysbzSpider
from app.spiders.jisuanke_spider import JisuankeSpider
from app.spiders.loj_spider import LojSpider
from app.spiders.luogu_spider import LuoguSpider
from app.spiders.nowcoder_spider import NowcoderSpider
from app.spiders.pintia_spider import PintiaSpider
from app.spiders.poj_spider import PojSpider
from app.spiders.vjudge_spider import VjudgeSpider
from app.spiders.zucc_spider import ZuccSpider


def submit_crawl_accept_problem_task(username=None, oj_id=None):
    from tasks import (crawl_accept_problem_task,
                       crawl_accept_problem_task_single)
    if username:
        user_list = [User.get_by_id(username)]
    else:
        user_list = User.search(status=1, page_size=-1)['data']
    if oj_id:
        oj_id_list = [OJ.get_by_id(oj_id)]
    else:
        oj_id_list = OJ.search(status=1, page_size=-1)['data']

    for user in user_list:
        for oj in oj_id_list:
            if oj.need_single_thread:
                crawl_accept_problem_task_single.delay(user.username, oj.id)
            else:
                crawl_accept_problem_task.delay(user.username, oj.id)


def crawl_accept_problem(username, oj_id):
    user = User.get_by_id(username)
    if not user:
        return
    oj = OJ.get_by_id(oj_id)
    if not oj:
        return
    oj_username = OJUsername.search(username=username, oj_id=oj_id)['data']
    if not oj_username:
        return

    oj_username = oj_username[0]
    oj_spider: BaseSpider = globals()[oj.name.title() + 'Spider']()

    accept_problems = dict()

    for i in AcceptProblem.search(username=username, page_size=-1)['data']:
        accept_problems["{}-{}".format(i.problem.oj.name, i.problem.problem_pid)] = \
            datetime.datetime.strftime(i.create_time, '%Y-%m-%d %H:%M:%S')

    res = oj_spider.get_user_info(oj_username, accept_problems.copy())
    if res['success']:
        oj_username.modify(last_success_time=datetime.datetime.now())
    crawl_accept_problems = res['data']
    print(crawl_accept_problems)

    deduplication_accept_problem = list()

    for i in crawl_accept_problems:
        pid = "{}-{}".format(i['oj'], i['problem_pid'])
        if i['accept_time'] is not None:
            if accept_problems.get(pid):
                if i['accept_time'] < accept_problems.get(pid):
                    deduplication_accept_problem.append(i)
            else:
                deduplication_accept_problem.append(i)
        else:
            if accept_problems.get(pid) is None:
                deduplication_accept_problem.append(i)

    print(len(deduplication_accept_problem))
    for i in deduplication_accept_problem:
        oj = OJ.get_by_name(i['oj'])
        problem = Problem.get_by_oj_id_and_problem_pid(oj.id, i['problem_pid'])
        submit_crawl_problem_rating_task(problem.id)
        accept_problem = AcceptProblem.get_by_username_and_problem_id(username, problem.id)
        accept_problem.modify(create_time=str_to_datetime(i['accept_time']), referer_oj_id=oj_id)


def submit_crawl_problem_rating_task(problem_id):
    from tasks import crawl_problem_rating_task
    crawl_problem_rating_task.delay(problem_id)


def crawl_problem_rating(problem_id):
    problem = Problem.get_by_id(problem_id)
    oj = OJ.get_by_id(problem.oj_id)
    try:
        oj_spider: BaseSpider = globals()[oj.name.title() + 'Spider']()
        rating = oj_spider.get_problem_info(problem.problem_pid)['rating']
    except:
        rating = DEFAULT_PROBLEM_RATING

    problem.modify(rating=rating)


def submit_crawl_course_info_task(course_id=None):
    from tasks import crawl_course_info_task
    if course_id is None:
        course_list = Course.search(page_size=-1)['data']
    else:
        course_list = [Course.get_by_id(course_id)]
    for course in course_list:
        if course.camp_oj.status == 1:
            crawl_course_info_task.delay(course.id)


def crawl_course_info(course_id):
    users = User.search(status=1, page_size=-1)['data']
    course = Course.get_by_id(course_id)
    spider_info = None
    if course.spider_username or course.spider_password:
        spider_info = {
            'username': course.spider_username,
            'password': course.spider_password
        }
    spider = globals()[course.camp_oj.name.title() + 'CampSpider'](spider_info)
    for contest in course.contests:
        res = spider.get_contest_meta(contest.contest_cid)
        if not res['success']:
            continue
        meta_info = res['data']
        max_pass = meta_info['max_pass']
        participants = meta_info['participants']
        contest.modify(
            max_pass=max_pass,
            participants=participants
        )
        for problem in meta_info['problems']:
            CampProblem.get_by_contest_id_and_problem_pid(contest.id, problem)
        for user in users:
            oj_username = CourseOJUsername.get_by_username_and_course_id(
                user.username,
                course_id
            )
            if oj_username is None:
                continue
            res = spider.get_user_info(contest.contest_cid, oj_username)
            if not res['success']:
                continue
            oj_username.modify(last_success_time=datetime.datetime.now())
            user_info = res['data']
            for problem_pid in user_info['pass_list']:
                problem = CampProblem.get_by_contest_id_and_problem_pid(
                    contest.id,
                    problem_pid
                )
                acp = CampAcceptProblem.get_by_username_and_problem_id(
                    user.username,
                    problem.id
                )
                if acp is None:
                    CampAcceptProblem.create(
                        username=user.username,
                        contest_id=contest.id,
                        problem_id=problem.id
                    )
            ac_cnt = len(user_info['pass_list'])
            rank = user_info['rank']
            rating = 200 * ((participants - rank + 1) / participants) * (ac_cnt / max_pass)
            rating = round(rating, 3)
            user_contest = UserContest.get_by_username_and_contest_id(
                user.username,
                contest.id
            )
            if user_contest is None:
                user_contest = UserContest.create(
                    username=user.username,
                    contest_id=contest.id
                )
            user_contest.modify(
                ac_cnt=len(user_info['pass_list']),
                rank=user_info['rank'],
                rating=rating
            )
