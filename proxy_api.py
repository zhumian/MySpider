import requests


def get():
    url = "http://193.112.92.24:9000/https/get"
    res = requests.get(url)
    return res.text


def delete(proxy_url):
    pass