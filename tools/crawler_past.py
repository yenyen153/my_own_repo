from datetime import timedelta
import logging
from tools.data_insert import *
from sqlalchemy.orm import sessionmaker
from tools.crawler_update import *
from sqlalchemy import create_engine
from app.schemas import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine("mysql+pymysql://user:password@localhost/ptt_db")
Session = sessionmaker(bind=engine)

one_year_ago = datetime.now() - timedelta(days=366)
one_year_ago_str = one_year_ago.strftime("%Y/%m/%d")

def fetch_board_posts(board_name):

    url = f"https://www.ptt.cc/bbs/{board_name}/index.html"

    while url:

        try:
            response = requests.get(url)
        except Exception as e:
            logging.error(e.with_traceback())
            break

        if response.status_code != 200:
            logger.error(f"Failed to fetch {url}, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('div.title a')

        for link in links:
            post_url = 'https://www.ptt.cc' + link['href']

            try:
                post = fetch_author(post_url)  # todo: 3/3 這邊的board_name改成for board_name in PTTboard的board_name
                post_date = datetime.strptime(post['date'], "%Y/%m/%d %H:%M:%S")
                try:
                    if 2024 <= post_date.year < 2025:
                        post['board'] = board_name
                        yield post

                    elif post_date.year < 2024:
                        logger.info(f"遇到其他年份的文章，結束爬取 {board_name} 版")
                        return

                except Exception as e:
                    print(f"錯誤來自{e}")
                    continue

            except Exception as e:
                print(e)
                continue

        next_page = soup.select('a.btn.wide')[1]['href']
        url = f"https://www.ptt.cc{next_page}"
# "Stock",
PTT_BOARDS = [ "Baseball", "Lifeismoney","home-sale", "MobileComm"]

def run_crawler():

    for board in PTT_BOARDS:
        logger.info(f"開始爬取 {board} 版的文章...")

        try:
            posts = fetch_board_posts(board)
        except Exception as e:
            logger.error(f"Error fetching posts from {board}: {str(e)}")
            continue

        for post in posts:
            try:
                PttPostModel(**post)
                data_check(Session, **post)
                data_in(Session, **post)
                logger.info(f"成功儲存文章: {post['title']}")

            except Exception as e:
                logger.error(f"Error processing post {post['title']}: {str(e)}")
                continue





if __name__ == "__main__":
    run_crawler()

