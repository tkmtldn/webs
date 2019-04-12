from src.collector import Collector
from src.config.req import config
from time import sleep


if __name__ == '__main__':
    clc = Collector()

    while True:
        clc.collect()
        print('Sleeping...')
        sleep(config.sleep_time)