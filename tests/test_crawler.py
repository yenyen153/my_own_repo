import pytest
import requests
from unittest.mock import MagicMock
from tools.crawler import fetch_posts

MOCK_HTML = """
<html>
    <body>
        <div class="r-ent">
            <div class="title">
                <a href="/bbs/NBA/M.1740027377.A.CDD.html">[新聞] 林書豪6年來首踏NBA球場！為何曾拒絕參加</a>
            </div>
            <div class="meta">
                <div class="author">access4096</div>
                <div class="date">2025/02/24 16:54:15</div>
            </div>
        </div>
    </body>
</html>
"""


@pytest.fixture
def mock_requests_get(mocker):

    mock_response = MagicMock()
    mock_response.text = MOCK_HTML
    mocker.patch("requests.Session.get", return_value=mock_response)


def test_fetch_posts(mock_requests_get):

    posts = fetch_posts("NBA")

    assert len(posts) == 1  # 確保回傳 1 篇文章
    assert posts[0]["board_name"] == "NBA"
    assert posts[0]["title"] == "[新聞] 林書豪6年來首踏NBA球場！為何曾拒絕參加"
    assert posts[0]["author_id"] == "access4096"
    assert posts[0]["link"] == "https://www.ptt.cc/bbs/NBA/M.1740027377.A.CDD.html"
    assert posts[0]["date"] == "2025/02/24 16:54:15"


def test_fetch_posts_real():

    posts = fetch_posts("NBA")

    assert requests.get("https://www.ptt.cc/bbs/NBA/index.html").status_code == 200
    assert posts[0]['board_name'] == 'NBA'
    assert "title" in posts[0]
    assert "author_id" in posts[0]
    assert "date" in posts[0]
    assert "link" in posts[0]
    assert len(posts) > 1
