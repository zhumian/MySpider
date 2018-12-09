import requests


def get():
    url = "http://localhost:8080/https/get"
    res = requests.get(url)
    return res.text


def delete(proxy_url):
    pass