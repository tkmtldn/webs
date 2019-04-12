import json
import os

from src.repository.mongodb import MongoRepository
from src.repository.rabbitmq import RabbitMqProvider


class Config:
    def __init__(self):
        self.tender_list_url = "https://tender.safmargroup.ru/trades.json"
        self.tender_url_id = "https://tender.safmargroup.ru/trades/{}.json"
        self.tender_url_template = "https://tender.safmargroup.ru/etp/trade/viewcontent.html?id={}&perspective=popup"
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.sleep_time = 30
        self.platform_timezone = "+0400"
        file_config = self._read_config_file()
        self.mongo = file_config['mongodb']
        self.rabbitmq = file_config['rabbitmq']
        self._repository = None
        self._rabbitmq = None


    def rabbitmq(self):
        if not self._rabbitmq:
            self._rabbitmq = RabbitMqProvider(config.rabbitmq['host'], config.rabbitmq['port'],
                                              config.rabbitmq['username'], config.rabbitmq['password'],
                                              config.rabbitmq['queue'])
        return self._rabbitmq


    def repository(self):
        if not self._repository:
            self._repository = MongoRepository(config.mongo['host'], config.mongo['port'], config.mongo['database'],
                                               config.mongo['collection'])
        return self._repository


    def _read_config_file(self):
        file_path = '%s/config.json' % self.root_dir
        try:
            with open(file_path, 'r', encoding='utf8') as cfg:
                return json.load(cfg)
        except Exception as e:
            raise ValueError('failed to load file `{}` with exception {}'.format(file_path, e))



config = Config()