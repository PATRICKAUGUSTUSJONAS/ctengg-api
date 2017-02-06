import webapp2
from bs4 import BeautifulSoup

from utils import *


class Attendance(webapp2.RequestHandler):

    @staticmethod
    def parse_attendance(doc):
        table = BeautifulSoup(doc, "html.parser")

        keys = ['course',
                'total',
                'attended',
                'percentage',
                'remark',
                'date']

        datasets = dict()
        datasets['attendance'] = list()

        datasets['name'] = table.find('strong').get_text().title()

        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(keys, (td.get_text() for td in row.find_all("td"))))
            datasets['attendance'].append(dataset)

        return datasets

    def get(self, fac_no):
        api_key = self.request.get("api_key")

        data = verify_api_key(api_key)
        if not data['error']:
            data = get_attendance(fac_no, data.pop('user'))

        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)
