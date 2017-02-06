import datetime

import webapp2
import xlrd
from bs4 import BeautifulSoup
from xlrd import XLRDError

from utils import *


class ClassAttendance(webapp2.RequestHandler):
    @staticmethod
    def parse_course(excel):
        book = xlrd.open_workbook(file_contents=excel)
        sheet = book.sheet_by_index(0)
        datasets = dict()

        course = str(sheet.cell(1, 0).value).replace('Course: ', '').strip()
        datasets['course'] = course[:course.find('(')].strip()
        datasets['course_name'] = course[course.find("(") + 1:course.find(")")].strip()

        try:
            date_generated = sheet.cell(0, 8).value
            datasets['date_generated'] = datetime.datetime(
                *xlrd.xldate_as_tuple(date_generated, book.datemode)).strftime("%B %d, %Y")
        except ValueError:
            pass
        try:
            date_upto = sheet.cell(1, 8).value
            datasets['date_upto'] = datetime.datetime(*xlrd.xldate_as_tuple(date_upto, book.datemode)).strftime(
                "%B %d, %Y")
        except ValueError:
            pass

        datasets['students'] = list()

        keys = ['fac_no', 'en_no', 'name', 'class', 's_no', 'delivered', 'attended', 'percent', 'remark']
        for row_index in xrange(3, sheet.nrows):
            data = dict(zip(keys, [cell.value for cell in sheet.row(row_index)]))

            for key in ['s_no', 'attended', 'delivered']:
                data[key] = int(float(data[key]))
            datasets['students'].append(data)

        return datasets

    @staticmethod
    def get_attendance_by_fetch(course):
        doc = urlfetch.fetch('http://ctengg.amu.ac.in/attendance/btech//' + course + '.XLSX')
        if '404' in doc.content:
            doc = urlfetch.fetch('http://ctengg.amu.ac.in/attendance/btech//' + course + '.XLS')

        try:
            data = ClassAttendance.parse_course(doc.content)
            data['error'] = False
            data['message'] = 'Successful'
        except XLRDError:
            data = dict()
            data['error'] = True
            data['message'] = 'Invalid Course'

        return data

    def get(self, course):
        course = course.upper()
        api_key = self.request.get("api_key")

        data = verify_api_key(api_key)
        if not data['error']:
            data = get_course_attendance(course, data.pop('user'))

        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)


class CompleteAttendance(webapp2.RequestHandler):
    @staticmethod
    def parse(doc):
        table = BeautifulSoup(doc, "html.parser")

        keys = ['course', 'teacher', 'date_of_upload', 'course', 'teacher', 'date_of_upload', 'course', 'teacher',
                'date_of_upload']

        datasets = dict()
        datasets['subjects'] = list()

        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(keys, (td.get_text() for td in row.find_all("td"))))
            datasets['subjects'].append(dataset)

        return datasets

    def get(self):
        api_key = self.request.get("api_key")

        data = verify_api_key(api_key)
        if not data['error']:
            data = get_complete_attendance(data.pop('user'))

        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)
