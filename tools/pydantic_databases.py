from pydantic import BaseModel, HttpUrl, Field, field_validator
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
import sqlalchemy as sa
from sqlalchemy.orm import relationship,declarative_base
import re

class PttPostModel(BaseModel):
    board_name: str  ##board_name
    title: str
    link: HttpUrl
    author_id: str
    date: str
    content: str
    @field_validator('date')
    @classmethod
    def validate_date(cls, value:str) -> str:
        if not re.search(r"\d{4}[/]\d{2}[/]\d{2}\s\d{2}[:]\d{2}[:]\d{2}", value):
            raise ValueError('wrong date format')
        return value


Base = declarative_base()
# engine = create_engine(
#     "mysql+pymysql://user:password@localhost/ptt_db"
# )


class PttPostsTable(Base):
    __tablename__ = "ptt_posts"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    board_id = sa.Column(sa.Integer, sa.ForeignKey("board.id"), nullable=False)
    author_id = sa.Column(sa.String(100), sa.ForeignKey("author.id"), nullable=False)
    title = sa.Column(sa.String(100), nullable=False)
    link = sa.Column(sa.String(255), unique=True, nullable=False)
    date = sa.Column(sa.String(20), nullable=False)
    content = sa.Column(sa.Text)

    board = relationship("BoardTable", back_populates="posts", foreign_keys=[board_id])
    author = relationship("AuthorTable", back_populates="posts", foreign_keys=[author_id])


class BoardTable(Base):
    __tablename__ = "board"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    board = sa.Column(sa.String(60), unique=True, nullable=False)
    url = sa.Column(sa.String(255), nullable=False)

    posts = relationship("PttPostsTable", back_populates="board", foreign_keys=[PttPostsTable.board_id])

class AuthorTable(Base):
    __tablename__ = "author"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    author_id = sa.Column(sa.String(100), unique=True, nullable=False)
    author_nickname = sa.Column(sa.String(100), nullable=False)
    #新增暱稱
    # posts_url = sa.Column(sa.String(255)) # todo: delete
    #
    posts = relationship("PttPostsTable", back_populates="author", foreign_keys=[PttPostsTable.author_id])



# Base.metadata.create_all(engine)












# class CrawlerLog(Base):
#     __tablename__ = "crawler_log"
#
#     id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
#     time = sa.Column(sa.Text)
#     message = sa.Column(sa.Text)