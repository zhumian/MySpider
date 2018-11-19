from urllib.request import urlopen
import requests, logging
from bs4 import BeautifulSoup
from db import DBSession, RentingHouse
from util import getNow, str2datetime
from proxyip import user_agent_list,get_headers
import proxyip


def find_zufang(url, start, proxy_url):
    res = None
    proxies = {
        'http': "http://" + proxy_url,
        'https:': "https://" + proxy_url
    }
    headers = get_headers()
    try:
        url = "%s?start=%s" % (url, start)
        res = requests.get(url, headers=headers, proxies=proxies)
    except Exception as e:
        logging.error(e)
    if res is None:
        pass
    elif res.status_code == 403:
        proxyip.proxy_url_pool.remove(proxy_url)
        logging.info("代理地址 : " + proxy_url + "已失效, 当前代理池地址数 : " + len(proxyip.proxy_url_pool))
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
                logging.error(e)
            session.close()


