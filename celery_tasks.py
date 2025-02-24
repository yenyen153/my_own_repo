from celery import Celery
from celery.schedules import crontab
from tools.crawler import run_crawler, fetch_posts
# import logging
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
    "fetch_ptt_every_min":{
        "task": "celery_tasks.test_crawler",
        "schedule": crontab(minute='*/1')
    }
}

@app.task
def test_crawler():
    run_crawler()