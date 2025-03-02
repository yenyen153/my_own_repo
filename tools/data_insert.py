from app.schemas import *
from app.models import *


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

def LogIn(Session,Crawlerfile):
    with Session() as session:
        with open(Crawlerfile, "r", encoding='utf-8') as log_file:
            logs = log_file.readlines()
            try:
                for log in logs:
                    match = re.match(r"([\d-]+ [\d:,]+) (.+)", log)

                    if match:
                        time = match.group(1)
                        message = match.group(2)
                        time_log = {'time':time, 'message':message}
                        session.add(CrawlerLog(**time_log))
            except Exception as e:
                pass

        session.commit()



