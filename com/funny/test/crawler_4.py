
''' crawler_4.py 

https://levirve.github.io/blog/2016/dcard-spider-python-package/
'''

from util import pretty_print
from bs4 import BeautifulSoup
import requests, time, urllib


def get_posts_on_page(url):
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    articles = soup.findAll("div", "r-ent")
    posts = list()
    for article in articles:
        push = article.find("div", "nrec").getText()
        title = article.find("div", "title").getText().strip()
        date = article.find("div", "meta").find("div", "date").getText()
        author = article.find("div", "meta").find("div", "author").getText()

        post = {"push": push, "title": title, "date": date, "author": author}
        posts.append(post)

    next_link = soup.find("div", "btn-group btn-group-paging").findAll("a", "btn")[1].get("href")
    
    return posts, next_link

INDEX = "https://www.ptt.cc/bbs/movie/index.html"

def get_pages(num: int):

    url = INDEX
    all_posts = list()
    for i in range(num):
        posts, next_link = get_posts_on_page(url)
        all_posts += posts
        url = urllib.parse.urljoin(INDEX, next_link)

    return all_posts

if __name__ == "__main__":        

    pages = 5

    start = time.time()
    for post in get_pages(pages):
        pretty_print(post['push'], post['title'], post['date'], post['author'])

    print("spend %f seconds" %(time.time() - start))