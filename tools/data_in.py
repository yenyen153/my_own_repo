from sqlalchemy.orm import sessionmaker
from tools.pydantic_databases import *


# Session = sessionmaker(bind=engine)

## name way change
def data_check(Session,**ptt_post): # todo: change name to define style
    with Session() as session:
        author = session.query(AuthorTable).filter_by(author_ptt_id=ptt_post['author_ptt_id']).first()
        board = session.query(BoardTable).filter_by(board=ptt_post['board_name']).first()


        if not author:

            session.add(AuthorTable(**{'author_nickname':ptt_post['author_nickname'],
                                    'author_ptt_id':ptt_post['author_ptt_id']}))
        if not board:

            session.add(BoardTable(**{'board':ptt_post['board_name'],
                                      'url': f"https://www.ptt.cc/bbs/{ptt_post['board_name']}/index.html" }))
        session.commit()
        session.close()

def data_in(Session,**ptt_post): # todo: change name to define style
    with Session() as session:
        post_link = session.query(PttPostsTable).filter_by(link=ptt_post['link']).first()
        author = session.query(AuthorTable).filter_by(author_ptt_id=ptt_post['author_ptt_id']).first()
        board = session.query(BoardTable).filter_by(board=ptt_post['board_name']).first()

        if not post_link:
            new_ptt_post = {
                "board_id":board.id,
                "title":ptt_post['title'],
                "link":ptt_post['link'],
                "author_id":author.id,
                "date":ptt_post['date'],
                "content":ptt_post['content']}
            session.add(PttPostsTable(**new_ptt_post))

        session.commit()
        session.close()






# def LogIn(Session,Crawlerlog):
#     with Session() as session:
#         with open(Crawlerlog, "r", encoding='utf-8') as log_file:
#             logs = log_file.readlines()
#             for log in logs:
#                 match = re.match(r"([\d-]+ [\d:,]+) (.+)", log)
#
#                 if match:
#                     time = match.group(1)
#                     message = match.group(2)
#                     time_log = {'time':time, 'message':message}
#                     session.add(CrawlerLog(**time_log))
#
#                 session.commit()
#                 session.close()

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
#     DataCheck(**test_data).
#     DataIn(**test_data)


