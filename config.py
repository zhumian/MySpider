import configparser

conf = configparser.ConfigParser()
conf.read('cfg.ini')


def db(key):
    return conf.get('db', key)