from sqlalchemy.orm import sessionmaker
from tools.pydantic_databases import *
import re

Session = sessionmaker(bind=engine)

def DataCheck(Session,**ptt_post):
    with Session() as session:
        author = session.query(AuthorTable).filter_by(name=ptt_post['author_name']).first()
        board = session.query(BoardTable).filter_by(board=ptt_post['board_id']).first()


        if not author:
            a = ptt_post['author_name']
            session.add(AuthorTable(**{'name':a,
                                        'posts_url':f"https://www.ptt.cc/bbs/{ptt_post['board_id']}/search?q=author%3A{a}"}))

        if not board:
            b = ptt_post['board_id']
            session.add(BoardTable(**{'board':b,
                                      'url': f'https://www.ptt.cc/bbs/{b}/index.html', }))
        session.commit()
        session.close()

def DataIn(Session,**ptt_post):
    with Session() as session:
        post_link = session.query(PttPostsTable).filter_by(link=ptt_post['link']).first()
        author = session.query(AuthorTable).filter_by(name=ptt_post['author_name']).first()
        board = session.query(BoardTable).filter_by(board=ptt_post['board_id']).first()

        if not post_link:
            new_ptt_post = {
                "board_id":board.id,
                "title":ptt_post['title'],
                "link":ptt_post['link'],
                "author_name":author.name,
                "date":ptt_post['date'],
                "content":ptt_post['content']}
            session.add(PttPostsTable(**new_ptt_post))

        session.commit()
        session.close()

def LogIn(Session,Crawlerlog):
    with Session() as session:
        with open(Crawlerlog, "r", encoding='utf-8') as log_file:
            logs = log_file.readlines()
            for log in logs:
                match = re.match(r"([\d-]+ [\d:,]+) (.+)", log)

                if match:
                    time = match.group(1)
                    message = match.group(2)
                    time_log = {'time':time, 'message':message}
                    session.add(CrawlerLog(**time_log))

                session.commit()
                session.close()

# def CrawlerLogIn(crawler_log):
#     with Session() as session:


# if __name__ == '__main__':
#
#     test_data = {
#         'board_id': 'stock',
#         'title': 'TEST_title_0224',
#         'link': 'https://www.ptt.cc/bbs/stock/index.html',
#         'date': '2019-09-22',
#         'author_name': 'test_stock_author',
#         'content': 'this is for stock teswt'
#     }
#
#     DataCheck(**test_data)
#     DataIn(**test_data)


