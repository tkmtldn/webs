from src.bill.http_worker import HttpWorker
from src.config.req import config
from src.bill.mapper import Mapper
from src.bill.parser import parser
from src.repository.mongodb import MongoRepository
from src.repository.rabbitmq import RabbitMqProvider


class Collector:
    def __init__(self):
        self._repository = None
        self._rabbitmq = None

    @property
    def repository(self):
        self._repository = MongoRepository(config.mongo['host'],
                                       config.mongo['port'],
                                       config.mongo['database'],
                                       config.mongo['collection'])
        return self._repository

    @property
    def rabbitmq(self):
        self._rabbitmq = RabbitMqProvider(config.rabbitmq['host'],
                                         config.rabbitmq['port'],
                                         config.rabbitmq['username'],
                                         config.rabbitmq['password'],
                                         config.rabbitmq['queue'])
        return self._rabbitmq

    def collect(self):
        params = {}
        tender_list = HttpWorker.get_tender_list(tender_list_params=params)
        for tender in tender_list['$top']['trades']['items']:
            url_id = tender['id']
            tender_info = HttpWorker.get_tender(url_id)
            self.process_tender(tender_info, tender_list, url_id)

    def process_tender(self, tender_info, tender_list, url_id):
        tenders = parser.parse(tender_info, tender_list, url_id)
        #print(tenders)
        for tender in tenders:
            dbmodel = self.repository.get_one(id=tender['number'])
            if dbmodel is not None and dbmodel['status'] == tender['tender_status']:
                print('{} already exists is MongoDB'.format(tender['number']))
                continue
            short_model = Mapper.tender_short_model(tender)
            self.repository.upsert(short_model)
            # print(short_model)
            notification = Mapper.map(tender)
            self.rabbitmq.publish(notification)
            # print(notification)