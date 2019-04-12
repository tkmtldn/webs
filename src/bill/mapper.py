from sharedmodel.module import Root, Field, Customer
from sharedmodel.module.enum import FieldType, Modification
from sharedmodel.module.table import Head, Cell
from src.bill.tools import get_utc, convert_datetime_str_to_timestamp


class Mapper:

    @classmethod
    def tender_short_model(cls, tender):
        return {
            '_id': tender['number'],
            'status': tender['tender_status'],
            'publication_date': tender['publicationDateTime']
        }

    @classmethod
    def convert_tender_status(cls, status):
        statuses = {"Неизвестно": 0,
                    "Прием заявок": 1,
                    "идёт приём заявок": 1,
                    "Работа комиссии": 2,
                    "Размещение завершено": 3,
                    "Размещение отменено": 4,
                    "Размещение не состоялось": 5,
                    "Исполнение завершено": 6,
                    "Исполняется": 7,
                    "Расторжение": 8}
        return statuses[status]

    @classmethod
    def map(cls, tender):
        model = {
            'platform': {
                'name': 'ЭТП ФГ Сафмар',
                'href': 'https://tender.safmargroup.ru'
            },
            'customer': {
                'name': 'АО "А101 ДЕВЕЛОПМЕНТ"',
                'region': 77,
                'inn': 5003097374,
                'kpp': 500301001,
                'guid': None
            },
            'id': tender['tender_id'],
            'globalSearch': tender['globalSearch'],
            'guaranteeApp': None,
            'status': Mapper.convert_tender_status(tender['tender_status']),
            'href': tender['tender_href'],
            'json': None,
            'maxPrice': None,
            'multilot': tender['multilot'],
            'number': tender['number'],
            'okdp': [],
            'okpd': [],
            'okpd2': [],
            'orderName': tender['orderName'],
            'organisationsSearch': tender['organisationsName'],
            'publicationDateTime': tender['publicationDateTime'],
            'region': 77,
            'submissonCloseDateTime': tender['submissonCloseDateTime'],
            'submissionStartDateTime': tender['submissionStartDateTime'],
            'tenderSearch': tender['globalSearch'],
            'timestamp': get_utc(),
            'version': 1
        }
        model['json'] = Mapper.get_json(model)
        return model

    @classmethod
    def get_json(cls, tender):
        return Root() \
            .add_general(
            Field(
                name='MaxPrice',
                type=FieldType.Price,
                value=None,
                displayName='Цена контракта'
            )) \
            .add_customer(
            Customer().set_properties(
                max_price=None,
                guarantee_app=None,
                guarantee_contract=None,
                customer_guid=tender['customer']['guid'],
                customer_name=tender['customer']['name']
            )) \
            .add_category(
                lambda c: c.set_properties(
                    name='ProcedureInfo',
                    displayName='Порядок размещения заказа',
                ).add_field(Field(
                    name='SubmissionCloseDateTime',
                    displayName='Дата окончания приема заявок',
                    value=tender['submissonCloseDateTime'],
                    type=FieldType.DateTime
                )))\
            .to_json()