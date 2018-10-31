from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from mysql import DBSession, RentingHouse
from util import getNow, str2datetime

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
}
proxy_dict = {
    "http": "http://219.135.170.187:45190/",
    "https": "http://219.135.170.187:45190/"
}


def spider(url, start):
    res = None
    try:
        url = "%s?start=%s" % (url, start)
        res = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
    if res is None:
        print("URL is not found")
    elif res.status_code == 403:
        print("403错误")
    else:
        bsObj = BeautifulSoup(res.text, "html.parser", from_encoding='utf-8')
        rows = bsObj.find("table", {"class": "olt"}).findAll("tr", {"class": ""})
        for row in rows:
            session = DBSession()
            tds = row.findAll("td")
            url = tds[0].find("a").get("href")
            publish_time = None
            try:
                content = urlopen(url)
            except Exception as e:
                print(e)
            if content is not None:
                try:
                    bsContentObj = BeautifulSoup(content.read(), 'html.parser', from_encoding='utf-8')
                    publish_time = str2datetime(bsContentObj.find("h3").find("span", {"class": "color-green"}).get_text())
                except Exception as e:
                    print(e)

            urlSplited = url.split("/")
            article_id = urlSplited[len(urlSplited) - 2]
            title = tds[0].find("a").get("title")
            author = tds[1].find("a").get_text()
            author_url = tds[1].find("a").get("href")

            item = RentingHouse(city='广州市', area='天河区', title=title, url=url, article_id=article_id,
                                author_url=author_url,
                                publish_time=publish_time, create_time=getNow())
            try:
                session.add(item)
                session.commit()
            except Exception as e:
                print(e)
            session.close()


def main():
    u = "https://www.douban.com/group/tianhezufang/discussion"
    count = 100
    for i in range(count):
        spider(u, i * 25)


if __name__ == "__main__":
    main()
