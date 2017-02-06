import json

from google.appengine.api import memcache

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


def get_item(key, user, cached, get_method, *args):
    data = memcache.get(key)

    if data is None or data['error'] or not cached:
        store_data = CacheData.get_by_id(key)

        if store_data is None or json.loads(store_data.data)['error'] or not cached:
            data = get_method(*args)
            if not data['error']:
                store_data = CacheData(id=key)
                store_data.request = key
                store_data.data = json.dumps(data)
                store_data.put()
        else:
            data = json.loads(store_data.data)
        data['user'] = user.username
        memcache.set(key, data)

    return data


def get_complete_attendance(user, use_stored=True):
    from CompleteAttendance import CompleteAttendance
    key = 'complete_attendance'
    return get_item(key, user, use_stored, CompleteAttendance.get_attendance_by_fetch)


def get_course_attendance(course, user, use_stored=True):
    from CompleteAttendance import ClassAttendance
    key = 'course_' + course
    return get_item(key, user, use_stored, ClassAttendance.get_attendance_by_fetch, course)


def get_result(fac_no, enrol_no, user, use_stored=True):
    from Result import Result
    key = 'result_' + fac_no.upper() + ':' + enrol_no.upper()
    return get_item(key, user, use_stored, Result.get_result_by_fetch, fac_no, enrol_no)


def get_attendance(fac_no, user, use_stored=True):
    from Attendance import Attendance
    key = 'attendance_' + fac_no.upper()
    return get_item(key, user, use_stored, Attendance.get_attendance_by_fetch, fac_no)

