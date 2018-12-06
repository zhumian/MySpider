from urllib.request import urlopen
import requests, logging
from bs4 import BeautifulSoup
from db import DBSession, Dbzf
from util.DateUtil import getNow, str2datetime
import util.HttpUtil as HttpUtil
import proxy_api
import balcklist


url_list = [
    {"area": "天河区", 'url': "https://www.douban.com/group/tianhezufang/discussion"},
    {"area": "海珠区", 'url': "https://www.douban.com/group/haizhuzufang/discussion"},
    {"area": "越秀区", 'url': "https://www.douban.com/group/yuexiuzufang/discussion"},
    {"area": "番禺区", 'url': "https://www.douban.com/group/panyuzufang/discussion"},
    {"area": "荔湾区", 'url': "https://www.douban.com/group/liwanzufang/discussion"},
    {"area": "3/5号线", 'url': "https://www.douban.com/group/huangpuzufang/discussion"},
    {"area": "天河区", 'url': "https://www.douban.com/group/606174/discussion"},
    {"area": None, 'url': "https://www.douban.com/group/maquezufang/discussion"},
    {"area": None, 'url': "https://www.douban.com/group/532699/discussion"},
]


def find_zufang(area, url, start, proxy_url):
    res = None
    proxies = {
        'http': "http://" + proxy_url,
        'https:': "https://" + proxy_url
    }
    headers = HttpUtil.getHeaders()
    try:
        url = "%s?start=%s" % (url, start)
        logging.info("开始爬取 : " + url)
        res = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    except Exception as e:
        logging.error(e)
        return False
    if res is None:
        return False
    elif res.status_code == 403:
        logging.info("403 forbidden : " + proxy_url)
        proxy_api.delete(proxy_url)
        return False
    else:
        bs = BeautifulSoup(res.text, "lxml")
        table = bs.find("table", {"class": "olt"})
        if table:
            rows = table.findAll("tr", {"class": ""})
            if rows:
                for row in rows:
                    session = DBSession()
                    tds = row.findAll("td")
                    url = tds[0].find("a").get("href")
                    publish_time = None
                    try:
                        content = urlopen(url)
                    except Exception as e:
                        logging.error(e)
                    if content is not None:
                        try:
                            bsContentObj = BeautifulSoup(content.read(), 'lxml')
                            publish_time = str2datetime(
                                bsContentObj.find("h3").find("span", {"class": "color-green"}).get_text())
                        except Exception as e:
                            logging.error(e)

                    urlSplited = url.split("/")
                    article_id = urlSplited[len(urlSplited) - 2]
                    title = tds[0].find("a").get("title")
                    author = tds[1].find("a").get_text()
                    author_url = tds[1].find("a").get("href")

                    if not validate(title):
                        continue

                    item = Dbzf(city='广州市', area=area, title=title, url=url, article_id=article_id,
                                author_url=author_url,
                                publish_time=publish_time, create_time=getNow())

                    try:
                        session.add(item)
                        session.commit()
                    except Exception as e:
                        logging.error(e)
            else:
                logging.info("找不到table")
                return False

    return True


def validate(title):
    for item in balcklist.blacklist:
        value = item.value
        if value in title:
            return False
    return True


