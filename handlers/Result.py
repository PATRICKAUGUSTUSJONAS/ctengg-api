import json
import webapp2
from bs4 import BeautifulSoup
from db.models import User
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache

class Result(webapp2.RequestHandler):

    def parse_result(self, page):
        table = BeautifulSoup(page, "html.parser")
        keys = ['course',
                'sessional_marks',
                'exam_marks',
                'total',
                'grace',
                'grades']


        credit_keys = ['faculty_number', 'enrolment', 'name', 'ec', 'spi', 'cpi']
        dataset = dict()


        cred_table = table.find('table', {'style':'width:100%;text-align:center;'})
        for row in cred_table.find_all('tr')[1:]:
            dataset= dict(zip(credit_keys, (m.get_text()for m in row.find_all('td'))))
        
        dataset['results'] = list()
        res_table = table.find('table', {'class':"table table-hover"})
        
        for row in res_table.find_all('tr')[1:]:
            x = dict(zip(keys, (m.get_text() for m in row.find_all('td'))))
            dataset['results'].append(x)
        
        return dataset

    def get_result(self, fac_no, enrol_no, user):
        key = 'result_'+fac_no.upper()
        data = memcache.get(key)

        if data is None:
            doc = urlfetch.fetch('http://ctengg.amu.ac.in/web/table_result.php?'+'fac='+fac_no+'&en='+enrol_no+'&prog=btech')
            try:
                data = self.parse_result(doc.content)
                data['error'] = False
                data['message'] = 'Successful'
            except AttributeError as e:
                data = dict()
                data['error'] = True
                data['message'] = 'Parse Error'
            data['user'] = user.username
            memcache.set(key, data, 1209600)

        return data

    def get(self):
        api_key = self.request.get('api_key')
        fac_no = self.request.get('fac')
        enrol_no = self.request.get('en')

        data = {'error':True, 'message':"URL must contain API Key : 'api_key', Faculty Number : 'fac' and Enrolment No : 'en'"}
        if api_key and fac_no and enrol_no:
            user = User.get_user(api_key)
            if user and not user.banned : 
                data = self.get_result(fac_no, enrol_no, user)
            elif user and user.banned :
                data = {'error':True, 'message':'API key is banned or not activated yet'}
            else :
                data = {'error':True, 'message':'No such API key in database'}
        
        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)