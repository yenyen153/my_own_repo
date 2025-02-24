import requests
from bs4 import BeautifulSoup
import datetime


PTT_BOARDS = ["Gossiping", "Stock", "C_Chat", "Baseball", "NBA"]
PTT_URL = "https://www.ptt.cc/bbs/{}/index.html"

session = requests.Session()
session.cookies.set("over18", "1")


## 爬取內文
def fetch_content(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    content = soup.find(id="main-content").text
    end_point = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
    content = content.split(end_point)
    return content[0]


def fetch_posts(board):
    res = session.get(PTT_URL.format(board))
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select(".r-ent")

    posts = []
    for article in articles:
        title_elem = article.select_one(".title a")
        if not title_elem:
            continue

        post_data = {
            "board_id": board,
            "title": title_elem.text,
            "link": "https://www.ptt.cc" + title_elem["href"],
            "author_name": article.select_one(".author").text,
            "date": article.select_one(".date").text
        }
        post_data["content"] = fetch_content(post_data["link"])

        posts.append(post_data)


    return posts


# ff = fetch_posts("Gossiping")
# print(ff[0])

# ## 爬取時間
# def fetch_date(link):
#     res = requests.get(link)
#     soup = BeautifulSoup(res.text, 'html.parser')
#
#     heads = soup.find_all('span', 'article-meta-value')
#     date = heads[3].text
#
#     return date



#
# #
# #
# #
#
#
#
# ## test new crawler
# def fetch_links(board):
#
#     res = session.get(PTT_URL.format(board))
#     soup = BeautifulSoup(res.text, "html.parser")
#     articles = soup.select(".r-ent")
#
#     links = []
#     for article in articles:
#         title_elem = article.select_one(".title a")
#         if not title_elem:
#             continue
#
#         links.append(f"https://www.ptt.cc{title_elem['href']}")
#
#     return links



# def parse_date(date_str):
#     current_year = datetime.datetime.now().year
#     month, day = map(int, date_str.split("/"))
#     return datetime.datetime(current_year, month, day)
