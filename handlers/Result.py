from google.appengine.api import urlfetch
import json
from python.result import parse_result
import webapp2

class Result(webapp2.RequestHandler):
    def get(self):
        fac_no = self.request.get('fac')
        enrol_no = self.request.get('en')
        doc = urlfetch.fetch('http://ctengg.amu.ac.in/web/table_result.php?'+'fac='+fac_no.upper()+'&en='+enrol_no.upper()+'&prog=btech')
        try:
            data = parse_result(doc.content)
            data['error'] = False
        except AttributeError as e:
            data = dict()
            data['error'] = True
        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_out)