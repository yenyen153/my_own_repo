import requests
from bs4 import BeautifulSoup
from datetime import datetime


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

## 爬取作者名字與id/版面／標題
def fetch_author(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    post_details = soup.select(".article-meta-value")
    details_list = []
    for author in post_details:
        details_list.append(author.text)

    posts_detail = {
        'board_name':details_list[1],
        'title':details_list[2],
        'author_id_':((details_list[0].split('('))[0]).rstrip(),
        'author_nickname':((details_list[0].split('('))[1]).rstrip(')'),
    }

    time_str = details_list[-1]
    dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
    formatted_time = dt.strftime("%Y/%m/%d %H:%M:%S")
    posts_detail['date'] = formatted_time

    return posts_detail


def fetch_posts(board):
    res = session.get(PTT_URL.format(board))
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select(".r-ent")

    posts = []
    for article in articles:
        title_elem = article.select_one(".title a")
        if not title_elem:
            continue


        post_link = f"https://www.ptt.cc{title_elem['href']}"
        post_detail = fetch_author(post_link)
        post_detail["content"] = fetch_content(post_link)
        post_detail["link"] = post_link

        posts.append(post_detail)


    return posts

post_detail = fetch_posts('Chiayi')
print(post_detail[1])


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
