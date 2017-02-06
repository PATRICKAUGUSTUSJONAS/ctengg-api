import json

import webapp2
from bs4 import BeautifulSoup
from google.appengine.api import memcache
from google.appengine.api import urlfetch

from db.models import CacheData
from db.models import RequestLog
from db.models import User


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

    @staticmethod
    def get_result_by_fetch(fac_no, enrol_no):
        doc = urlfetch.fetch(
            'http://ctengg.amu.ac.in/web/table_resultnew.php?' + 'fac=' + fac_no + '&en=' + enrol_no + '&prog=btech')
        try:
            data = Result.parse_result(doc.content)
            data['error'] = False
            data['message'] = 'Successful'
        except AttributeError:
            data = dict()
            data['error'] = True
            data['message'] = 'Parse Error'

        return data

    @staticmethod
    def get_result(fac_no, enrol_no, user, use_stored=True):
        key = 'result_' + fac_no.upper() + ':' + enrol_no.upper()
        data = memcache.get(key)

        if data is None or not use_stored:
            store_data = CacheData.get_by_id(key)
            if store_data is None or not use_stored:
                data = Result.get_result_by_fetch(fac_no, enrol_no)
                store_data = CacheData(id=key)
                store_data.request = key
                store_data.data = json.dumps(data)
                store_data.put()
            else:
                data = json.loads(store_data.data)
            data['user'] = user.username
            memcache.set(key, data)

        return data

    @staticmethod
    def log(fac_no, enrol_no):
        fac_no = fac_no.upper()
        enrol_no = enrol_no.upper()
        key = fac_no + ':' + enrol_no
        request_log = RequestLog.get_by_id(key)
        if request_log is None:
            request_log = RequestLog(id=key)
            request_log.attendance = False
            request_log.requests = request_log.requests + 1
            request_log.data = key
            request_log.put()
        else:
            request_log.attendance = False
            request_log.data = key
            request_log.requests = request_log.requests + 1
            request_log.put()

    def get(self):
        api_key = self.request.get('api_key')
        fac_no = self.request.get('fac')
        enrol_no = self.request.get('en')

        data = {'error': True,
                'message': "URL must contain API Key : 'api_key', Faculty Number : 'fac' and Enrolment No : 'en'"}
        if api_key and fac_no and enrol_no:
            user = User.get_user(api_key)
            if user and not user.banned:
                data = Result.get_result(fac_no, enrol_no, user)
                # Result.log(fac_no, enrol_no)
            elif user and user.banned:
                data = {'error': True, 'message': 'API key is banned or not activated yet'}
            else:
                data = {'error': True, 'message': 'No such API key in database'}

        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)
