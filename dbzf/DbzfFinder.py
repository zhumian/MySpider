from urllib.request import urlopen

import logging
import requests
from bs4 import BeautifulSoup

import balcklist
import proxy_api
import util.HttpUtil as HttpUtil
from db import DBSession, Dbzf
from util.DateUtil import getNow, str2datetime


def find_zufang(area, url, start):
    res = None
    proxy_url = proxy_api.get()
    proxies = {
        'https:': "https://" + proxy_url
    }
    headers = HttpUtil.getHeaders()
    try:
        url = "%s?start=%s" % (url, start)
        logging.info("start spider [page:{url}] [proxy:{proxy}]".format(url=url, proxy=proxy_url))
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
                logging.info("table not found")
                return False

    return True


def validate(title):
    for item in balcklist.blacklist:
        value = item.value
        if value in title:
            return False
    return True


def run(area, url, start):
    find_zufang(area, url, start)


