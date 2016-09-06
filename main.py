# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch
import json
import parse_result


def parse(doc):
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


class Result(webapp2.RequestHandler):
    def get(self):
    	fac_no = self.request.get("fac")
    	en_no  = self.request.get("en")

    	data = dict()
    	data['error'] = False

    	if fac_no and en_no :
    		doc = urlfetch.fetch('http://ctengg.amu.ac.in/web/table_result.php?'+'fac='+fac_no+'&en='+en_no+'&prog=btech')

    		try:
    			data = parse_result.parse_result(doc.content)
    		except AttributeError as e:
    			data = dict()
    			data['error'] = True
    	else :
    		data['error'] = True

        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_out)
        

class IndexHandler(webapp2.RequestHandler):
	def get(self):
		self.redirect('static/index.html')
		

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=IndexHandler, name='home'),
    webapp2.Route(r'/index.html', handler=IndexHandler, name='home'),
    webapp2.Route(r'/attendance/<fac_no>', handler=Attendance, name='attendance'),
    webapp2.Route(r'/result/btech', handler = Result, name = 'result')
])
