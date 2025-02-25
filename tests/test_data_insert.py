from tools.data_in import DataCheck, DataIn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from tools.pydantic_databases import PttPostsTable, AuthorTable, BoardTable, CheckModel


Base = declarative_base()

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

PttPostsTable.metadata.create_all(engine)
BoardTable.metadata.create_all(engine)
AuthorTable.metadata.create_all(engine)


def test_data_insert():

    Session = sessionmaker(bind=engine)

    test_post = {
        "board_id": "NBA",
        "title": "[新聞] 林書豪6年來首踏NBA球場！為何曾拒絕參加",
        "link": "https://www.ptt.cc/bbs/NBA/M.1740027377.A.CDD.html",
        "author_name": "Test_Author",
        "date": "2/20",
        "content": "這是測試內容"
    }

    with Session() as session:

        CheckModel(**test_post)

        DataCheck(Session,**test_post)

        DataIn(Session,**test_post)

        post = session.query(PttPostsTable).filter_by(link=test_post["link"]).first()
        board = session.query(BoardTable).first()
        author = session.query(AuthorTable).first()

        assert post.title == test_post["title"]
        assert post.author_name == test_post["author_name"]
        assert post.board_id is not None
        assert board.id is not None
        assert author.name is not None