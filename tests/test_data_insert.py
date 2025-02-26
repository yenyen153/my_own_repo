from tools.data_in import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from tools.pydantic_databases import PttPostsTable, AuthorTable, BoardTable, PttPostModel


Base = declarative_base()

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

PttPostsTable.metadata.create_all(engine)
BoardTable.metadata.create_all(engine)
AuthorTable.metadata.create_all(engine)


def test_data_insert():

    Session = sessionmaker(bind=engine)

    test_post = {
        "board_name": "NBA",
        "title": "[新聞] 林書豪6年來首踏NBA球場！為何曾拒絕參加",
        "link": "https://www.ptt.cc/bbs/NBA/M.1740027377.A.CDD.html",
        "author_ptt_id": "Test_Author_ID",
        "author_nickname": "Test_Author_Nickname",
        "date": "2025/02/26 14:38:12",
        "content": "這是測試內容"
    }

    with Session() as session:

        PttPostModel(**test_post) # todo : 這個要修改格式

        data_check(Session,**test_post)

        data_in(Session,**test_post)

        post = session.query(PttPostsTable).first()
        board = session.query(BoardTable).first()
        author = session.query(AuthorTable).first()

        assert post.title == test_post["title"]
        assert post.board_id is not None
        assert board.id is not None
        assert author.author_nickname == test_post["author_nickname"]
        assert author.author_ptt_id == test_post["author_ptt_id"]
