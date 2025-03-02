from fastapi.testclient import TestClient
from app.user import app
import pytest

client = TestClient(app)


def test_create_post(db_session):
    """ 測試新增文章，但不會真的存進 MariaDB """
    new_post = {
        "title": "Test Post",
        "link": "https://www.ptt.cc/bbs/TestBoard/M.1234567890.A.BBB.html",
        "date": "2024/03/02 12:45:22",
        "content": "This is a test post.",
        "board_name": "TestBoard",
        "author_ptt_id": "test123",
        "author_nickname": "TestUser"
    }

    response = client.post("/api/posts", json=new_post)

    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"


def test_get_posts(db_session):
    """ 測試獲取文章，但不會真的影響資料庫 """
    response = client.get("/api/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
