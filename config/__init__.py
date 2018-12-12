from configparser import ConfigParser
import os
cp = ConfigParser()
path = os.path.dirname(os.path.realpath(__file__))
file = path + os.sep + "config.ini"
cp.read(file)


def db(key):
    return cp.get('db', key)