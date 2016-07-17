from google.appengine.api import urlfetch
import json
from python.attendance import parse
import webapp2

class Attendance(webapp2.RequestHandler):
    def get(self, fac_no):
        doc = urlfetch.fetch('http://ctengg.amu.ac.in/web/table.php?id='+fac_no)

        try:
            data = parse(doc.content)
            data['error'] = False
        except AttributeError as e:
            data = dict()
            data['error'] = True

        data['fac'] = fac_no.upper()
        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)