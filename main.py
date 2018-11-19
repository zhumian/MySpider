from proxyip import find_proxy_ip
import threading, logging, random, time
import proxyip
from douban_zufang import find_zufang
logging.basicConfig(level=logging.INFO)



def start_find_proxy_ip():
    logging.info("开始爬取西刺代理IP")
    url = 'http://www.xicidaili.com/nn/'
    for num in range(3000):
        find_proxy_ip(url, num)
        time.sleep(5)


def start_find_douban_zufang():
    logging.info("开始搜寻豆瓣租房信息")
    url = "https://www.douban.com/group/tianhezufang/discussion"
    page = 0
    while True:
        if len(proxyip.proxy_url_pool) > 4 :
            proxy_url = random.choice(proxyip.proxy_url_pool)
            find_zufang(url, page * 25, proxy_url)
            page += 1
            time.sleep(5)
        else:
            time.sleep(10)


if __name__ == '__main__':
    threads = []
    t2 = threading.Thread(target=start_find_douban_zufang)
    t1 = threading.Thread(target=start_find_proxy_ip)
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        t.start()