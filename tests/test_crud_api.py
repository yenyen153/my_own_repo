import pytest

@pytest.fixture()
def test_create_post(test_client,property_payload):
    response = test_client.post("/api/posts", json=property_payload)
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "title for testing"
    return data

# 測試回傳最新50篇的功能
def test_get_posts(test_client):
    response = test_client.get("/api/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 測試用id查找文章
def test_get_post_by_id(test_client,test_create_post):
    data = test_create_post
    response = test_client.get(f"/api/posts/{data['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == data["id"]
    assert response.json()['title'] == "title for testing"
    assert response.json()['link'] == "https://linkfortesting.com/"
    assert response.json()['content'] == "content for testing"

# 測試用條件查找文章
def test_get_statistics(test_client,property_payload):
    test_client.post("/api/posts", json=property_payload)
    board_name = property_payload["board_name"]
    response = test_client.get(f"/api/statistics?board_name={board_name}")
    assert response.status_code == 200
    assert "文章總篇數" in response.json()

# 測試用id刪除文章
def test_delete_post(test_client, test_create_post):
    post_id = test_create_post['id']
    response = test_client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Post deleted"}

# 測試刪除不存在的文章 應該要有的反應
def test_get_nonexistent_post(test_client):
    response = test_client.get("/api/posts/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

# 測試post錯誤格式文章 應該要有的反應
def test_create_post_invalid_date(test_client):
    wrong_data = {
        "board_name": "Gossiping",
        "author_ptt_id": "test_user",
        "author_nickname": "Test User",
        "title": "錯誤的日期格式",
        "content": "這是一篇測試文章",
        "link": "https://www.ptt.cc/bbs/Gossiping/M.1234567890.A.html",
        "date": "2025-03-03 12:00:00"  # 錯誤格式 應該是2025/03/03
    }
    response = test_client.post("/api/posts", json=wrong_data)
    assert response.status_code == 422

# 測試更新文章 然後看文章是不是真的被更新
def test_update_post(test_client, test_create_post):
    post_data = test_create_post
    post_id = post_data["id"]

    updated_data = {
        "board_name": "update board name",
        "author_ptt_id": "update author ptt id",
        "author_nickname": "Updated author nickname",
        "title": "update title",
        "content": "update content",
        "link": "https://updatelink.html",
        "date": "2025/03/03 13:00:00"
    }

    response = test_client.put(f"/api/posts/{post_id}", json=updated_data)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["title"] == "update title"
    assert response_json["content"] == "update content"