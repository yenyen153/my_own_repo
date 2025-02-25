from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
import sqlalchemy as sa
from sqlalchemy.orm import relationship,declarative_base


class CheckModel(BaseModel):
    board_id: str
    title: str
    link: HttpUrl
    author_name: str
    date: str
    content: str


Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://user:password@localhost/ptt_db"
)


class PttPostsTable(Base):
    __tablename__ = "ptt_posts"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    board_id = sa.Column(sa.Integer, sa.ForeignKey("board.id"), nullable=False)
    author_name = sa.Column(sa.String(100), sa.ForeignKey("author.name"), nullable=False)
    title = sa.Column(sa.String(100), nullable=False)
    link = sa.Column(sa.String(255), unique=True, nullable=False)
    date = sa.Column(sa.String(20), nullable=False)
    content = sa.Column(sa.Text)

    board = relationship("BoardTable", back_populates="posts", foreign_keys=[board_id])
    author = relationship("AuthorTable", back_populates="posts", foreign_keys=[author_name])

class BoardTable(Base):
    __tablename__ = "board"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    board = sa.Column(sa.String(60), unique=True, nullable=False)
    url = sa.Column(sa.String(255), nullable=False)

    posts = relationship("PttPostsTable", back_populates="board", foreign_keys=[PttPostsTable.board_id])

class AuthorTable(Base):
    __tablename__ = "author"

    name = sa.Column(sa.String(100), primary_key=True)
    posts_url = sa.Column(sa.String(255))

    posts = relationship("PttPostsTable", back_populates="author", foreign_keys=[PttPostsTable.author_name])


class CrawlerLog(Base):
    __tablename__ = "crawler_log"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    time = sa.Column(sa.Text)
    message = sa.Column(sa.Text)

Base.metadata.create_all(engine)
