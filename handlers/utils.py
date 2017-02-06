import json

from google.appengine.api import memcache

from Attendance import Attendance
from CompleteAttendance import ClassAttendance
from CompleteAttendance import CompleteAttendance
from Result import Result
from db.models import CacheData


def verify_page(doc):
    data = dict()
    data['error'] = False
    if '404' in doc:
        data['error'] = True
        data['message'] = 'Server is down! Please try again'
    elif 'alert' in doc:
        data['error'] = True
        data['message'] = (doc.split("'"))[1].split("'")[0]

    return data


def get_complete_attendance(user, use_stored=True):
    key = 'complete_attendance'
    data = memcache.get(key)

    if data is None or not use_stored:
        store_data = CacheData.get_by_id(key)
        if store_data is None or use_stored:
            data = CompleteAttendance.get_attendance_by_fetch()
            store_data = CacheData(id=key)
            store_data.request = key
            store_data.data = json.dumps(data)
            store_data.put()
        else:
            data = json.loads(store_data.data)
        data['user'] = user.username
        memcache.set(key, data)

    return data


def get_course_attendance(course, user, use_stored=True):
    key = 'course_' + course
    data = memcache.get(key)

    if data is None or not use_stored:
        store_data = CacheData.get_by_id(key)
        if store_data is None or not use_stored:
            data = ClassAttendance.get_attendance_by_fetch(course)
            store_data = CacheData(id=key)
            store_data.request = key
            store_data.data = json.dumps(data)
            store_data.put()
        else:
            data = json.loads(store_data.data)
        data['user'] = user.username
        memcache.set(key, data)

    return data


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


def get_attendance(fac_no, user, use_stored=True):
    key = 'attendance_' + fac_no.upper()
    data = memcache.get(key)

    if data is None or data['error'] or not use_stored:
        store_data = CacheData.get_by_id(key)

        if store_data is None or json.loads(store_data.data)['error'] or not use_stored:
            data = Attendance.get_attendance_by_fetch(fac_no)
            if not data['error']:
                store_data = CacheData(id=key)
                store_data.request = key
                store_data.data = json.dumps(data)
                store_data.put()
        else:
            data = json.loads(store_data.data)
        data['fac'] = fac_no.upper()
        data['user'] = user.username
        memcache.set(key, data)

    return data

