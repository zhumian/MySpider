import datetime


def getNow():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def str2datetime(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

