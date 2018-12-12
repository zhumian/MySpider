import logging
import time
from dbzf.DbzfScheduler import run as DbzfRun

format = "%(asctime)s - [%(levelname)s] - [%(funcName)s] - %(message)s"
logging.basicConfig(level=logging.INFO, format=format)

if __name__ == '__main__':
    DbzfRun(1)

    while True:
        time.sleep(5)




