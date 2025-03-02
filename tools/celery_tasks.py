from celery import Celery
from celery.schedules import crontab
from tools.crawler_update import run_crawler, fetch_posts
import logging

#
# logging.basicConfig(
#     filename="crawler.log",
#     level=logging.INFO,
#     filemode='a',
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     encoding='utf-8'
# )

app = Celery("task",
             broker="redis://localhost:6379/0",
             broker_connection_retry_on_startup=True)

app.conf.beat_schedule = {
    "fetch_ptt_every_min": {
        "task": "celery_tasks.test_crawler",
        "schedule": crontab(minute='*/1')
    }
}


@app.task
def test_crawler():
    run_crawler()

app = Celery("task",
             broker="redis://localhost:6379/0",
             broker_connection_retry_on_startup=True)

app.conf.beat_schedule = {
    "fetch_ptt_every_min":{
        "task": "main.run_crawler",
        "schedule": crontab(minute='*/5')
    }
}

my_logger = logging.getLogger()

logging.basicConfig(
    filename="crawler.log",
    level=logging.INFO,
    filemode='w',
    format="%(asctime)s %(message)s",
    encoding='utf-8'
)



# Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://user:password@localhost/ptt_db"
)
#
# PttPostsTable.metadata.create_all(engine)
# BoardTable.metadata.create_all(engine)
# AuthorTable.metadata.create_all(engine)
# CrawlerLog.metadata.create_all(engine)
#
Session = sessionmaker(bind=engine)


# db = SessionLocal()

# @app.task
# def run_crawler():
PTT_BOARDS = ["Gossiping", "Stock", "C_Chat", "Baseball", "NBA"]

for board in PTT_BOARDS:
    my_logger.info(f"正在爬取{board}")
#
# with Session() as session:
#     LogIn(session, 'crawler.log')  # 傳入 session 作為參數

# for board in PTT_BOARDS:
#
#     links = fetch_link(board)
#
#     for link in links:
#         try:
#             post = fetch_author(link)
#             PttPostModel(**post)
#             data_check(Session, **post)
#             data_in(Session, **post)
#         except Exception as e:
#             print(e)

for board in PTT_BOARDS:
    links = fetch_link(board)

    for link in links:
        post = fetch_author(link)
        post['board'] = board
        try:


                data_check(Session, **post)

                data_in(Session, **post)
                print('success')

        except Exception as e:
            print(link)