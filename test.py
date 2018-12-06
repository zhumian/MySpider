import requests
import proxy_api
import util.HttpUtil as HttpUtil


def run():
    user_agent = HttpUtil.getUserAgent()
    headers = {'User-agent': user_agent}
    proxy_url = "115.46.77.103:8123"
    proxies = {
        'http': "http://" + proxy_url,
        'https:': "https://" + proxy_url
    }
    url = "http://www.baidu.com"
    res = requests.get(url, headers=headers, proxies=proxies)
    print(res.status_code)


def demo():
    text = '【次卧出租】猎德 三房一厅'
    key = '次卧'
    if key in text:
        print("有")


if __name__ == "__main__":
    run()