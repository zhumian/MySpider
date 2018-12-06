import requests
import json
import random


def get():
    url = "http://193.112.92.24:5010/get_all"
    res = requests.get(url)
    list = json.loads(res.content)
    return random.choice(list)


def delete(proxy_url):
    url = "http://193.112.92.24:5010/delete?proxy=" + proxy_url
    requests.get(url)