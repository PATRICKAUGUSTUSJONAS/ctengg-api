import json
import webapp2
from bs4 import BeautifulSoup
from db.models import User
from db.models import RequestLog
from db.models import CacheData
from google.appengine.api import urlfetch
from google.appengine.api import memcache

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

    @staticmethod
    def get_attendance_by_fetch(fac_no):
        doc = urlfetch.fetch('http://ctengg.amu.ac.in/web/table.php?id='+fac_no)
        try:
            data = Attendance.parse_attendance(doc.content)
            data['error'] = False
            data['message'] = 'Successful'
        except AttributeError:
            data = dict()
            data['error'] = True
            data['message'] = 'Parse Error'

        return data

    @staticmethod
    def get_attendance(fac_no, user, use_stored = True):
        key = 'attendance_'+fac_no.upper()
        data = memcache.get(key)

        if data is None or not use_stored:
            store_data = CacheData.get_by_id(key)
            if store_data is None or not use_stored:
                data = Attendance.get_attendance_by_fetch(fac_no)
                store_data = CacheData(id = key)
                store_data.request = key
                store_data.data = json.dumps(data)
                store_data.put()
            else:
                data = json.loads(store_data.data)
            data['fac'] = fac_no.upper()
            data['user'] = user.username
            memcache.set(key, data)

        return data

    @staticmethod
    def log(fac_no):
        fac_no = fac_no.upper()
        request_log = RequestLog.get_by_id(fac_no)
        if request_log is None:
            request_log = RequestLog(id = fac_no)
            request_log.attendance = True
            request_log.requests = request_log.requests + 1
            request_log.data = fac_no
            request_log.put()
        else:
            request_log.attendance = True
            request_log.data = fac_no
            request_log.requests = request_log.requests + 1
            request_log.put()

    def get(self, fac_no):
        api_key = self.request.get("api_key")

        data = {'error':True, 'message':"URL must contain API Key : 'api_key'"}
        if api_key:
            user = User.get_user(api_key)
            if user and not user.banned : 
                data = Attendance.get_attendance(fac_no, user)
                #Attendance.log(fac_no)
            elif user and user.banned :
                data = {'error':True, 'message':'API key is banned or not activated yet'}
            else :
                data = {'error':True, 'message':'No such API key in database'}
        
        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)