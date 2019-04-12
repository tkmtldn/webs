import requests
from bs4 import BeautifulSoup
from src.config.req import config


class HttpWorker:
    @classmethod
    def get_tender_list(cls, tender_list_params=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        res = requests.get(config.tender_list_url, headers=headers, params=tender_list_params)
        return res.json()

    @classmethod
    def get_tender(cls, page_id):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        detailed_url = config.tender_url_template.format(page_id)
        res = requests.get(detailed_url, headers=headers).content
        return res

    @classmethod
    def bs4_scrap(cls, tender_info):
        # (example https://tender.safmargroup.ru/etp/trade/viewcontent.html?id=175381923&perspective=popup)
        soup = BeautifulSoup(tender_info, "html.parser")

        level_a = soup.find_all('tr')
        level_a = [element.text.strip().split('      ') for element in level_a]
        from_tender_bs4 = {i[0]: i[1] for i in level_a if len(i) == 2}

        for index, elem in enumerate(soup.findAll("div", "alert alert-warning")):
            from_tender_bs4.setdefault('Изменения', []).append(elem.text.strip().split('\r')[0])

        return from_tender_bs4