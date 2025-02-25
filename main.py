from tools.crawler import  fetch_posts
from sqlalchemy.orm import sessionmaker
import requests
from tools.data_in import *
from tools.pydantic_databases import *
import logging

logging.basicConfig(
    filename="crawler.log",
    level=logging.INFO,
    filemode='a',
    format="%(asctime)s %(message)s",
    encoding='utf-8'
)

logger = logging.getLogger()


Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://user:password@localhost/ptt_db"
)

PttPostsTable.metadata.create_all(engine)
BoardTable.metadata.create_all(engine)
AuthorTable.metadata.create_all(engine)
CrawlerLog.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

PTT_BOARDS = ["Gossiping", "Stock", "C_Chat", "Baseball", "NBA"]
PTT_URL = "https://www.ptt.cc/bbs/{}/index.html"

for board in PTT_BOARDS:
    posts = fetch_posts(board)
    logger.info(f"正在爬取{board}")

    for post in  posts:
        try:
            CheckModel(**post)
            DataCheck(Session,**post)
            DataIn(Session,**post)
        except:
            pass
        ##先PASS 如果有要記錄再增加

LogIn(Session, 'crawler.log')
