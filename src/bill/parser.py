import copy
from src.config.req import config
from src.bill.tools import convert_datetime_str_to_timestamp
from src.bill.http_worker import HttpWorker


class Parser:
    def parse(self, tender_info, tender_list, url_id):

        #1 Parsing collected data via BeatifulSoup
        from_tender_bs4 = HttpWorker.bs4_scrap(tender_info)

        #2 Collecting data from main json object

        for i in tender_list['$top']['trades']['items']:
            if i['id'] == url_id:
                from_tender_json = i

        #3 Collecting data to one object
        inf = dict()
        lots_quantity = from_tender_json['lots']

        platform_href = 'https://tender.safmargroup.ru'
        number = from_tender_json['registeredNumber']
        organisationsName = from_tender_json['owner']['title']
        organisationsAddress = from_tender_bs4['Почтовый адрес']
        organisationsPerson = from_tender_bs4['Контактное лицо']
        organisationsPhone = from_tender_bs4['Номер контактного телефона']
        organisationsEmail = from_tender_bs4['Адрес электронной почты']
        publicationDateTime = from_tender_bs4['Начало приема предложений']
        submissonCloseDateTime = from_tender_json['bidSubmissionEndDate']
        submissionStartDateTime = from_tender_bs4['Начало приема предложений']
        submissonConfirmationEndTime = from_tender_bs4['Окончание подтверждения участия']
        tender_href = platform_href + from_tender_json['viewLocation']
        tender_status = from_tender_bs4['Статус торгов'].strip()

        try:
            deliveryTime = from_tender_bs4['Сроки поставки товаров, выполнения работ, оказания услуг']
        except KeyError:
            deliveryTime = None
        try:
            deliveryPlace = from_tender_bs4['Место (адрес) поставки товаров, выполнения работ, оказания услуг']# Место поставки
        except KeyError:
            deliveryPlace = None
        try:
            changes = from_tender_bs4['Изменения'] # Изменения
        except KeyError:
            changes = None

        inf['number'] = number
        inf['organisationsName'] = organisationsName
        inf['organisationsAddress'] = organisationsAddress
        inf['organisationsPerson'] = organisationsPerson
        inf['organisationsPhone'] = organisationsPhone
        inf['organisationsEmail'] = organisationsEmail
        inf['publicationDateTime'] = convert_datetime_str_to_timestamp(publicationDateTime,
                                                                                config.platform_timezone)
        inf['submissonCloseDateTime'] = submissonCloseDateTime
        inf['submissionStartDateTime'] = convert_datetime_str_to_timestamp(submissionStartDateTime,
                                                                                config.platform_timezone)
        inf['submissonConfirmationEndTime'] = convert_datetime_str_to_timestamp(submissonConfirmationEndTime,
                                                                                config.platform_timezone)
        inf['tender_href'] = tender_href
        inf['tender_status'] = tender_status
        inf['deliveryTime'] = deliveryTime
        inf['deliveryPlace'] = deliveryPlace
        inf['changes'] = changes

        if len(lots_quantity) == 1:
            inf['multilot'] = False
            tender_id = number + "_" + str(1)
            orderName = from_tender_json['title']
            globalSearch = tender_id + " " + orderName + " " + organisationsName
            inf['tender_id'] = tender_id
            inf['orderName'] = orderName
            inf['globalSearch'] = globalSearch
            return [inf]
        else:
            multilot_inf = []
            inf['multilot'] = True
            for id, index in enumerate(lots_quantity, start=1):
                new_inf = copy.deepcopy(inf)
                tender_id = number + "_" + str(id)
                orderName = index['title']
                globalSearch = tender_id + " " + orderName + " " + organisationsName
                new_inf['tender_id'] = tender_id
                new_inf['orderName'] = orderName
                new_inf['globalSearch'] = globalSearch
                multilot_inf.append(new_inf)
            return multilot_inf


parser = Parser()