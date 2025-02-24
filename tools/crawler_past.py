import requests
from bs4 import BeautifulSoup
import datetime
import json
import time

PTT_Insurance_URL = "https://www.ptt.cc/bbs/Insurance/index{}.html"
PTT_BASE_URL = "https://www.ptt.cc"

ONE_YEAR_AGO = datetime.datetime.now() - datetime.timedelta(days=365)

session = requests.Session()
session.cookies.set("over18", "1")


def get_last_page():
    res = session.get(PTT_Insurance_URL.format(''))
    soup = BeautifulSoup(res.text, 'html.parser')
    prev_page_btn = soup.select_one('.btn-group-paging a:nth-child(2)')
    if prev_page_btn:
        last_page = int(prev_page_btn['href'].split('index')[1].split('.html')[0]) + 1
        return last_page
    return None


def parse_date(date_str):
    current_year = datetime.datetime.now().year
    month, day = map(int, date_str.split("/"))
    post_date = datetime.datetime(current_year, month, day)

    if post_date > datetime.datetime.now():
        post_date = post_date.replace(year=current_year - 1)

    return post_date


def fetch_page_posts(page_num):
    url = PTT_Insurance_URL.format(page_num)
    res = session.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select(".r-ent")

    posts = []
    for article in articles:
        title_elem = article.select_one(".title a")
        if not title_elem:
            continue

        post_url = PTT_BASE_URL + title_elem["href"]
        title = title_elem.text
        author_elem = article.select_one(".author")
        date_elem = article.select_one(".date")

        if not author_elem or not date_elem:
            continue

        author = author_elem.text
        post_date = parse_date(date_elem.text)

        if post_date < ONE_YEAR_AGO:
            return None  # 結束爬取

        posts.append({
            "board": "Insurance",
            "title": title,
            "author": author,
            "date": post_date.strftime("%Y-%m-%d"),
            "url": post_url
        })

    return posts


def crawl_insurance_past_year():
    last_page = get_last_page()
    if last_page is None:
        print("無法取得 PTT Insurance 版頁數")
        return

    all_posts = []
    for page in range(last_page, 0, -1):
        print(f"正在爬取 PTT Insurance 第 {page} 頁...")
        posts = fetch_page_posts(page)
        if posts is None:
            break
        all_posts.extend(posts)
        time.sleep(1)

    with open("insurance_posts.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=4)

    print(f"爬取完成，共獲取 {len(all_posts)} 篇文章")


if __name__ == "__main__":
    crawl_insurance_past_year()
