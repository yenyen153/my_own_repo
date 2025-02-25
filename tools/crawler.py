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

## 爬取作者
def fetch_author(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    post_details = soup.select(".article-meta-value")
    detail = []
    for author in post_details:
        detail.append(author.text)

    posts_detail = {
        'board_name':detail[1],
        'title':detail[2],
        'date':detail[-1],
        'author_id_in_ptt':, # todo : seperate aurthor id and author name
        'author_name_in_ptt':,
        'link':, # todo : link will from fetch_posts's post_data['link']
        'content':  # todo : content from fetch_content (upper function)
    }

    return detail


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

detail = fetch_author('https://www.ptt.cc/bbs/home-sale/M.1740472551.A.199.html')
print(detail)

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
