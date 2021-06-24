# mainly copied from https://github.com/billvsme/videoSpider, thanks very much

from celery import Celery
from celery.signals import worker_process_init
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from app.config.secure import SQLALCHEMY_DATABASE_URI


def create_new_engine(database_url=SQLALCHEMY_DATABASE_URI):
    db_engine = create_engine(database_url)
    return db_engine


engine = create_new_engine()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

'''Why use a dict save engine and session?
Because using multiprocess, you should create new connection to database.
In the begin, I see the
http://docs.sqlalchemy.org/en/latest/core/pooling.html#using-connection-pools-with-multiprocessing,
and use above approaches, but on the new process start, have some error.
'''
sqla = {
    'engine': engine,
    'session': session
}


def create_new_sqla(database_url=SQLALCHEMY_DATABASE_URI):
    new_engine = create_new_engine(database_url)
    session_ = sessionmaker(bind=new_engine)
    new_session = session_()

    sqla['engine'] = new_engine
    sqla['session'] = new_session

    return sqla


@worker_process_init.connect
def new_process(**args):
    create_new_sqla()


celery_app = Celery('tasks')
celery_app.config_from_object('app.config.secure')
