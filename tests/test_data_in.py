import pytest
from tools.data_in import *
from tools.pydantic_databases import *
from sqlalchemy.orm import sessionmaker
from pytest_mock import MockFixture

MOCK_DATA={
    'board_id': 'stock',
    'title': 'TEST_title_0223',
    'link': 'https://www.ptt.cc/bbs/stock/index.html',
    'date': '2025-02-23',
    'author_name': 'test_stock_author',
    'content': 'this is for stock test'},



Session = sessionmaker(bind=engine)
session = Session()


def CheckModelTest(MOCK_DATA):

    CheckModel(**MOCK_DATA)
    DataCheck(**MOCK_DATA)
    DataIn(**MOCK_DATA)

    title_result = session.query(PttPostsTable).filter_by(title=MOCK_DATA['title']).first()

    assert title_result == 'TEST_title_0223'