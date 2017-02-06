import webapp2
from bs4 import BeautifulSoup

from utils import *


class Result(webapp2.RequestHandler):
    @staticmethod
    def parse_result(page):
        table = BeautifulSoup(page, "html.parser")
        keys = ['course',
                'course_name',
                'sessional_marks',
                'exam_marks',
                'total',
                'highest',
                'class_average',
                'grace',
                'grades',
                'subject_rank']

        credit_keys = ['faculty_number', 'enrolment', 'name', 'ec', 'spi', 'cpi']
        dataset = dict()

        cred_table = table.find('table', {'style': 'width:100%;text-align:center;'})
        for row in cred_table.find_all('tr')[1:]:
            dataset = dict(zip(credit_keys, (m.get_text() for m in row.find_all('td'))))

        dataset['results'] = list()
        res_table = table.find('table', {'class': "table table-hover"})

        for row in res_table.find_all('tr')[1:]:
            x = dict(zip(keys, (m.get_text() for m in row.find_all('td'))))
            dataset['results'].append(x)

        return dataset

    def get(self):
        api_key = self.request.get('api_key')
        fac_no = self.request.get('fac')
        enrol_no = self.request.get('en')

        data = verify_api_key(api_key)
        if not data['error']:
            user = data.pop('user')
            data = {'error': True,
                    'message': "URL must contain Faculty Number : 'fac' and Enrolment No : 'en'",
                    'user': user.username}
            if fac_no and enrol_no:
                data = get_result(fac_no, enrol_no, user)

        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)
