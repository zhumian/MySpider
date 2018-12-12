from apscheduler.schedulers.background import BackgroundScheduler

from dbzf.DbzfFinder import run as DbzfRun

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


def run(pageNum):
    sched = BackgroundScheduler()
    for i in url_list:
        area = i['area']
        url = i['url']
        for p in range(pageNum):
            sched.add_job(DbzfRun, 'interval', minutes=5, args=(area, url, p * 25))
    sched.start()