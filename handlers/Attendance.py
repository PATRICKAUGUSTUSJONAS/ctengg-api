import webapp2
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch

from db.models import User
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

    @staticmethod
    def get_attendance_by_fetch(fac_no):
        doc = urlfetch.fetch('http://ctengg.amu.ac.in/web/table.php?id=' + fac_no)

        data = verify_page(doc.content)
        if data['error']:
            return data

        try:
            data = Attendance.parse_attendance(doc.content)
            data['error'] = False
            data['message'] = 'Successful'
        except AttributeError:
            data['error'] = True
            data['message'] = 'Parse Error'

        return data

    def get(self, fac_no):
        api_key = self.request.get("api_key")

        data = {'error': True, 'message': "URL must contain API Key : 'api_key'"}
        if api_key:
            user = User.get_user(api_key)
            if user and not user.banned:
                data = get_attendance(fac_no, user)
            elif user and user.banned:
                data = {'error': True, 'message': 'API key is banned or not activated yet'}
            else:
                data = {'error': True, 'message': 'No such API key in database'}

        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)
