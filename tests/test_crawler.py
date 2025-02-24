import pytest
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from tools.crawler import fetch_posts

MOCK_HTML = """
<html>
    <body>
		<div class="r-ent">
			<div class="nrec"><span class="hl f3">23</span></div>
			<div class="title">
				<a href="/bbs/NBA/M.1740027377.A.CDD.html">[新聞] 林書豪6年來首踏NBA球場！為何曾拒絕參加</a>
			</div>
			<div class="meta">
				<div class="author">access4096</div>
				<div class="article-menu">
					<div class="trigger">&#x22ef;</div>
					<div class="dropdown">
						<div class="item"><a href="/bbs/NBA/search?q=thread%3A%5B%E6%96%B0%E8%81%9E%5D&#43;%E6%9E%97%E6%9B%B8%E8%B1%AA6%E5%B9%B4%E4%BE%86%E9%A6%96%E8%B8%8FNBA%E7%90%83%E5%A0%B4%EF%BC%81%E7%82%BA%E4%BD%95%E6%9B%BE%E6%8B%92%E7%B5%95%E5%8F%83%E5%8A%A0">搜尋同標題文章</a></div>
						<div class="item"><a href="/bbs/NBA/search?q=author%3Aaccess4096">搜尋看板內 access4096 的文章</a></div>
					</div>
				</div>
				<div class="date">2/20</div>
				<div class="mark"></div>
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
    assert posts[0]["board_id"] == "NBA"
    assert posts[0]["title"] == "[新聞] 林書豪6年來首踏NBA球場！為何曾拒絕參加"
    assert posts[0]["author_name"] == "access4096"
    assert posts[0]["link"] == "https://www.ptt.cc/bbs/NBA/M.1740027377.A.CDD.html"
    assert posts[0]["date"] == "2/20"



@pytest.fixture
def test_fetch_posts_work():

    posts = fetch_posts('NBA')

    assert requests.get("https://www.ptt.cc/bbs/NBA/index.html").status_code == 200
    assert posts[0]['board_id'] == 'NBA'
    assert "title" in posts[0]
    assert "author_name" in posts[0]
    assert "date" in posts[0]
    assert "link" in posts[0]
    assert len(posts) > 1

