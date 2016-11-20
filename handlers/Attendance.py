import json
import webapp2
from bs4 import BeautifulSoup
from db.models import User
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache

class Attendance(webapp2.RequestHandler):

    def parse_attendance(self, doc):
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

    def get_attendance(self, fac_no, user):
        key = 'attendance_'+fac_no.upper()
        data = memcache.get(key)

        if data is None:
            doc = urlfetch.fetch('http://ctengg.amu.ac.in/web/table.php?id='+fac_no)
            try:
                data = self.parse_attendance(doc.content)
                data['error'] = False
                data['message'] = 'Successful'
            except AttributeError as e:
                data = dict()
                data['error'] = True
                data['message'] = 'Parse Error'
            data['fac'] = fac_no.upper()
            data['user'] = user.username
            memcache.set(key, data, 1209600)

        return data

    def get(self, fac_no):
        api_key = self.request.get("api_key")

        data = {'error':True, 'message':"URL must contain API Key : 'api_key'"}
        if api_key:
            user = User.get_user(api_key)
            if user and not user.banned : 
                data = self.get_attendance(fac_no, user)
            elif user and user.banned :
                data = {'error':True, 'message':'API key is banned or not activated yet'}
            else :
                data = {'error':True, 'message':'No such API key in database'}
        
        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)