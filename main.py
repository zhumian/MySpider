import logging
import threading
import time
import random
from apscheduler.schedulers.background import BackgroundScheduler
import balcklist
import proxy_api
from douban_zufang import find_zufang, url_list

logging.basicConfig(level=logging.INFO)


def start_find_douban_zufang(area, url, size):
    page = 0
    while page < size:
        proxy_url = proxy_api.get()
        if proxy_url:
            result = find_zufang(area, url, page * 25, proxy_url)
            if result:
                page += 1
            time.sleep(random.randint(10, 20))


if __name__ == '__main__':
    balcklist.loadBlackList()
    sched = BackgroundScheduler()
    for i in url_list:
        area = i['area']
        url = i['url']
        sched.add_job(start_find_douban_zufang, 'interval', minutes=15, args=(area, url, 3))
    sched.start()

    for i in url_list:
        area = i['area']
        url = i['url']
        start_find_douban_zufang(area=area, url=url, size=1)

    while True:
        time.sleep(5)
    '''
    threads = []
    for i in url_list:
        area = i['area']
        url = i['url']
        t = threading.Thread(target=start_find_douban_zufang, args=(area, url, 1))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    '''



