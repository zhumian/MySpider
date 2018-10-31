from datetime import datetime
import threading, random, requests, logging, os
from bs4 import BeautifulSoup


def write(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write("\n")


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = []
        for s in f.readlines():
            text.append(s.strip())
    return text


def get_headers():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    return headers


def check_ip(url, ip):
    headers = get_headers()
    proxies = {
        "http": "http://" + ip,
        "https": "https://" + ip
    }
    try:
        res = requests.get(url=url, proxies=proxies, headers=headers, timeout=5)
        status_code = res.status_code
        if(status_code == 200):
            return True
        else:
            print("ip地址无效")
            return False
    except Exception as e:
        print(e)
        return False


def find_proxy_ip(type, page_num, target_url, path):
    list = {
        "1": "http://www.xicidaili.com/nt/",
        "2": "http://www.xicidaili.com/nn/",
        "3": "http://www.xicidaili.com/wn/",
        "4": "http://www.xicidaili.com/wt/"
    }
    url = list[str(type + 1)] + str(page_num + 1)
    headers = get_headers()
    html = requests.get(url=url, headers=headers, timeout=5,)
    soup = BeautifulSoup(html.text, 'lxml')
    all = soup.findAll("tr", {"class": "odd"})
    for item in all:
        tds = item.findAll("td")
        ip_address = tds[1].text + ":" + tds[2].text
        if(check_ip(target_url, ip_address)):
            write(path=path, text=ip_address)
            print(ip_address)


def main():
    print(os.path.dirname(__file__))
    target_url = "https://www.baidu.com/"
    path = os.path.dirname(__file__) + '/ip.txt'
    start = datetime.now()
    threads = []
    for type in range(4):
        for page_num in range(3):
            t = threading.Thread(target=find_proxy_ip(type=type, page_num=page_num, target_url=target_url, path=path))
            threads.append(t)
    logging.info("开始爬取代理IP")
    print("开始爬取代理IP")
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    logging.info("爬取代理IP完成")
    print("爬取代理IP完成")
    end = datetime.now()


if __name__ == "__main__":
    main()